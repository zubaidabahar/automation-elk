from assertpy import assert_that
from google.oauth2 import service_account
from google.cloud.container import ClusterManagerClient
from support.config_sa import project_id, region, cluster_name, namespace
from kubernetes import client
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

def test_01_test_cluster_connection():
    print(cluster)


def test_02_get_cluster_name():
    print(cluster.name)
    assert_that(cluster.name).is_equal_to(cluster_name)

def test_03_test_deployment():
    client.Configuration.set_default(configuration)
    v1 = client.ExtensionsV1beta1Api()
    deployment = v1.list_namespaced_deployment(namespace)
    dep_length = len(deployment.items)
    assert_that(dep_length).is_greater_than(0)

def test_04_test_services():
    client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()
    services = v1.list_namespaced_service(namespace)
    serv_length = len(services.items)
    assert_that(serv_length).is_greater_than(2)

