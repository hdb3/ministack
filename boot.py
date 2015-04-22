import time
from os import environ as env
# import novaclient
import novaclient.client
nova = novaclient.client.Client("1.1", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                # region_name=env['OS_REGION_NAME']
                                )

print(nova.servers.list())


image = nova.images.find(name="centos7")
flavor = nova.flavors.find(name="m1.large")
net = nova.networks.find(label="mgmt-net")
nics = [{'net-id': net.id}]
instance = nova.servers.create(name="c99", image=image,
                                      flavor=flavor, key_name="dell4", nics=nics)

print instance.id
print("Sleeping for 5s after create command")
time.sleep(5)
print(nova.servers.list())
