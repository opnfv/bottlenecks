from kubernetes import client, config
from utils.k8s_setup import k8s_utils

import os
import datetime
import uuid

import utils.logger as log
import yaml
import argparse

LOG = log.Logger(__name__).getLogger()

parser = argparse.ArgumentParser(description='kubestone (k8s stress) tests')
parser.add_argument("-c", "--TEST_CASE",
                    help="The path of test case in form of yaml")
args = parser.parse_args()
TEST_CASE = args.TEST_CASE
TEST_CASE_NAME, TEST_CASE_FORMAT = os.path.splitext(
    os.path.basename(TEST_CASE))
OUT_FILE = ("/tmp/bottlenecks_kubestone_" +
            TEST_CASE_NAME + "_" + str(uuid.uuid4()) + ".out")


def test_step_result(num, success_num, during_seconds, result):
    testdata = {}
    test_result = {}
    test_result["number_of_deployments"] = float(num)
    test_result["success_deployments"] = success_num
    test_result["success_rate"] = success_num / num
    test_result["duration_time"] = during_seconds
    test_result["result"] = result
    testdata["data_body"] = test_result
    testdata["testcase"] = TEST_CASE_NAME
    return testdata


def main():
    INSTALLER_TYPE = os.getenv("INSTALLER_TYPE")
    K8S_CONFIG_PATH = os.getenv("K8S_CONFIG_PATH")
    K8S_APPS_API_VERSION = os.getenv("K8S_APPS_API_VERSION")
    K8S_CORE_API_VERSION = os.getenv("K8S_CORE_API_VERSION")
    # Get k8s config. If provided in the path indicated by
    # K8S_CONFIG_PATH, only return the path.
    if K8S_CONFIG_PATH:
        k8s_utils.get_config_path(
            K8S_CONFIG_PATH=K8S_CONFIG_PATH)
    else:
        if INSTALLER_TYPE:
            K8S_CONFIG_PATH = k8s_utils.get_config_path(
                INSTALLER_TYPE=INSTALLER_TYPE)
        else:
            k8s_utils.get_config_path()

    config.load_kube_config(K8S_CONFIG_PATH)

    # Initiate api clients
    if K8S_APPS_API_VERSION:
        apps_api = k8s_utils.get_apps_api(K8S_APPS_API_VERSION)
    else:
        apps_api = k8s_utils.get_apps_api()

    if K8S_CORE_API_VERSION:
        core_api = k8s_utils.get_core_api(K8S_CORE_API_VERSION)
    else:
        core_api = k8s_utils.get_core_api()

    # Read test case in the form of yaml
    test_case_file = open(TEST_CASE, 'r')
    test_case_yaml = yaml.load(test_case_file)
    if test_case_yaml['template']:
        if test_case_yaml['template'].lower() == 'none':
            deployment_yaml = test_case_yaml
        else:
            deployment_file = open(test_case_yaml['template'], 'r')
            deployment_yaml = yaml.load(deployment_file)
    else:
        deployment_yaml = test_case_yaml

    name = deployment_yaml['metadata']['name']
    namespace = deployment_yaml['namespace']
    body = client.V1Deployment()
    body.api_version = deployment_yaml['apiVersion']
    body.kind = deployment_yaml['kind']
    body.metadata = deployment_yaml['metadata']
    body.spec = deployment_yaml['spec']
    pretty = True

    # Create namespace
    namespace_existed = k8s_utils.get_namespace_status(namespace)
    if namespace_existed[0] == 0 and \
            'exception' not in namespace_existed[1].lower():
        namespace_read = core_api.read_namespace(namespace, pretty=pretty)
        LOG.info('Namespace {} already exist: \n{}'.format(
            namespace, namespace_read))
    else:
        namespace_body = client.V1Namespace()
        namespace_body.metadata = {'name': namespace}
        namespace_created = core_api.create_namespace(
            namespace_body, pretty=pretty)
        LOG.info('Namespace has been created:\n{}'.format(
            namespace_created))

    # create deployment
    deployment_existed = k8s_utils.get_deployment_status(name, namespace)
    if deployment_existed[0] == 0 and \
            'exception' not in deployment_existed[1].lower():
        deployment_read = apps_api.read_namespaced_deployment(
            name, namespace, pretty=pretty)
        LOG.info('Deployment {}@{} already exist.'.format(name, namespace))
        LOG.info('Discription of this deployment is:\n{}'.format(
            deployment_read))
    else:
        deployment_created = apps_api.create_namespaced_deployment(
            namespace, body, pretty=pretty)
        LOG.info('Deployment has been created:\n{}'.format(
            deployment_created))

    # Run the test
    scaling_steps = deployment_yaml['scaling_steps'].split(',')
    for step in scaling_steps:
        start_time = datetime.datetime.now()

        step = int(step)
        body.spec['replicas'] = step
        api_response = apps_api.patch_namespaced_deployment_scale(
            name, namespace, body, pretty=pretty)
        LOG.info("Deployment replicas is to be scaled to: %s" % step)
        pods_number = k8s_utils.get_available_pods(name, namespace)
        while pods_number != step:
            pods_number = k8s_utils.get_available_pods(name, namespace)
            LOG.info("Number of available pods are {} out of {}".format(
                pods_number, step))
        api_response = apps_api.read_namespaced_deployment_scale(
            name, namespace, pretty=pretty)
        LOG.info(
            "Deployment {}-scaling finished:\n{}".format(
                step, api_response))

        end_time = datetime.datetime.now()
        duration_seconds = (start_time - end_time).seconds
        if pods_number == step:
            criteria = 'PASS'
        else:
            criteria = 'FAIL'
        test_result_body = test_step_result(
            step, pods_number, duration_seconds, criteria)
        k8s_utils.write_json(test_result_body, OUT_FILE)
    if api_response:
        LOG.info("Deployment scaling test has been successfuly executed.")
    LOG.info("Testing results writen in: {}".format(OUT_FILE))
    return


if __name__ == '__main__':
    main()
