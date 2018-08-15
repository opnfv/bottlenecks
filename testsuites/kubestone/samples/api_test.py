from kubernetes import client, config, watch
import k8s_utils
import utils.logger as log
import yaml
LOG = log.Logger(__name__).getLogger()

config.load_kube_config("/tmp/config")
v1 = client.CoreV1Api()
namespace = v1.list_namespace
k8s_utils.watch_namespace(namespace)
count = 10

k8s_utils.watch_namespace(namespace, count, stop='default', request_timeout=0)


# request_timeout var shouldn't be _request_timeout
def w_ns(namespace, count=3, request_timeout=60):
    w = watch.Watch()
    LOG.info(w)
    LOG.info(namespace)
    LOG.info(w.stream(namespace, _request_timeout=request_timeout))
    for event in w.stream(namespace, _request_timeout=request_timeout):
        LOG.info("Event: %s %s" %
                 (event['type'], event['object'].metadata.name))
        count -= 1


w_ns(namespace)

w = watch.Watch()
LOG.info(w)
LOG.info(namespace)
LOG.info(w.stream(namespace, _request_timeout=60))
for event in w.stream(namespace, _request_timeout=60):
    LOG.info("Event: %s %s" %
             (event['type'], event['object'].metadata.name))


namespace = 'default'
pod_file = open('./pod_sample.yaml', 'r')
pod_yaml = yaml.load(pod_file)
print(pod_yaml)
print("\n")
# Although 4 vars of V1PodTemplate are optional indicated in k8s api docs,
# we still need to clearly assign the values body.metadata and body.template.
body = client.V1PodTemplate()
# apiVerion could be v1
#body.api_version = pod_yaml['apiVersion']
# Should be podTemplate otherwise there will be kind error
#body.kind = pod_yaml['kind']
body.metadata = pod_yaml['metadata']
body.template = {'spec':pod_yaml['spec']}
print(body)
print("\n")
pretty = 'true'
api_response = v1.create_namespaced_pod_template(namespace, body, pretty=pretty)
print(api_response)
print("\n")
