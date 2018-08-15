from kubernetes import client, config
from utils.k8s_setup import k8s_utils

import os
import time

import utils.logger as log
import yaml
import argparse

LOG = log.Logger(__name__).getLogger()

parser = argparse.ArgumentParser(description='kubestone (k8s stress) tests')
parser.add_argument("-c", "--TEST_CASE",
                    help="The path of test case in form of yaml")
args = parser.parse_args()


def main():
    INSTALLER_TYPE = os.getenv("INSTALLER_TYPE")
    K8S_CONFIG_PATH = os.getenv("K8S_CONFIG_PATH")
    K8S_APPS_VERSION = os.getenv("K8S_APPS_VERSION")
    TEST_CASE = args.TEST_CASE

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

    if K8S_APPS_VERSION:
        apps_api = k8s_utils.get_apps_api(K8S_APPS_VERSION)
    else:
        apps_api = k8s_utils.get_apps_api()

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
    exact = True
    export = True

    deployment_existed = apps_api.read_namespaced_deployment(
        name, namespace, pretty=pretty, exact=exact, export=export)
    if deployment_existed:
        LOG.info('Deployment {} already exist.'.format(name))
        LOG.info('Discription of this deployment is:\n{}'.format(
            deployment_existed))
    else:
        deployment_created = apps_api.create_namespaced_deployment(
            namespace, body, pretty=pretty)
        LOG.info('Deployment has been created:\n{}'.format(
            deployment_created))

    scaling_steps = deployment_yaml['scaling_steps'].split(',')
    for steps in scaling_steps:
        steps = int(steps)
        body.spec['replicas'] = steps
        api_response = apps_api.patch_namespaced_deployment_scale(
            name, namespace, body, pretty=pretty)
        LOG.info("Deployment replicas is scaled to: %s" % steps)
        time.sleep(10)
        api_response = apps_api.read_namespaced_deployment_scale(
            name, namespace, pretty=pretty)
        LOG.info(
            "Discription of the scaled deployment is:\n{}".format(
                api_response))
    if api_response:
        LOG.info("Deployment scaling test has been successfuly executed.")
    return


if __name__ == '__main__':
    main()
