from distutils.command.config import config

from assertpy import assert_that
from google.oauth2 import service_account
from google.cloud.container import ClusterManagerClient
from support.config_sa import project_id, region, cluster_name, namespace
from kubernetes import client, config
import os


dir = os.path.dirname(__file__)
sa_file = os.path.join(dir, 'gcp_sa_test.json')

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
credentials = service_account.Credentials.from_service_account_file(sa_file, scopes=SCOPES)
cluster_manager_client = ClusterManagerClient(credentials=credentials)
cluster = cluster_manager_client.get_cluster(project_id, region, cluster_name)
configuration = client.Configuration()
configuration.host = "https://" + cluster.endpoint + ":443"
configuration.api_key = {"authorization": "Bearer " + credentials.token}
client.Configuration.set_default(configuration)

# Tests
def test_01_test_cluster_connection():
    print(cluster)


def test_02_get_cluster_name():
    print(cluster.name)
    assert_that(cluster.name).is_equal_to(cluster_name)


"""
def test_03_list_all_pods():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod(namespace=namespace)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def test_04_test_services():
   config.load_kube_config()

   v1 = client.CoreV1Api()
   services = v1.list_namespaced_service(namespace=namespace)
   serv_length = len(services.items)
   assert_that(serv_length).is_greater_than(2)
"""






