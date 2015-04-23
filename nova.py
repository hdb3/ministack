import time
import sys
import traceback
from os import environ as env
# import novaclient
from pprint import pprint
import novaclient.client
nova = novaclient.client.Client("1.1", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                )



def list ():
    print "list"
    print(nova.servers.list())

def boot ():
    image = nova.images.find(name="centos7")
    flavor = nova.flavors.find(name="m1.large")
    net = nova.networks.find(label="mgmt-net")
    nics = [{'net-id': net.id}]
    instance = nova.servers.create(name="c99", image=image, flavor=flavor, key_name="dell4", nics=nics)

    print instance.id
    print("Sleeping for 5s after create command")
    time.sleep(5)
    print(nova.servers.list())

def check_keypair(name):
    try:
        return not ( nova.keypairs.get(name).deleted )
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

# boot()
# net()
# pprint.pprint ( nova )

# print "checking keypair dell4"
# print check_keypair('dell4')

pprint(dir(nova))
pprint(dir(nova.servers))
pprint(nova.servers.list())
print dir(nova.servers.list()[0])

