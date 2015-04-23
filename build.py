import time
import sys
import traceback
from os import environ as env
import os
from pprint import pprint
from neutronclient.v2_0 import client
import novaclient.client
from spec import spec

def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

credentials = get_credentials()
neutron = client.Client(**credentials)

def netlist():
    netw = neutron.list_networks()
    pprint(netw['networks'])

nova = novaclient.client.Client("1.1", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                # region_name=env['OS_REGION_NAME']
                                )

server_list = {}
net_list = {}

for server in nova.servers.list():
    server_list[server] = None

for net in neutron.list_networks()['networks']:
  # print net['name'], net['id']
  net_list[net['name']] = net['id']


class BuildError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

def boot_template(image,flavor,keypair):
    try:
        _image=nova.images.find(name=image)
        if (not _image):
            raiseBuildError("image %s not found" % image)
        _flavor=nova.flavors.find(name=flavor)
        if (not _flavor):
            raiseBuildError("flavor %s not found" % flavor)
        _keypair=nova.keypairs.find(name=keypair)
        if (not _keypair):
            raiseBuildError("keypair %s not found" % keypair)
        return (_image,_flavor,_keypair)
    except novaclient.exceptions.NotFound:
        print "Not found: " , sys.exc_value
        return None
    except:
        traceback.print_exc()
        print "Unexpected error:", sys.exc_info()[0]


def boot ():
    print "boot"
    print(nova.servers.list())
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

# netlist()
srv_template = boot_template("centos7","m1.large","dell4")
pprint(srv_template)
srv_template2 = boot_template("centos6","m1.big","dell9")
pprint(srv_template2)


print "Checking global parameters"

print "checking keypair" , spec['keypair']
print check_keypair(spec['keypair'])


print "checking default network name" , spec['default network name']
default_net = nova.networks.find(label=spec['default network name'])
print "checking external network name" , spec['external network name']
external_net = nova.networks.find(label=spec['external network name'])

net_builder = {}
host_builder = []

if ( spec['Networks']):
    print " building networks"
    for net in spec['Networks']:
        print "building network ", net['name'] , net['subnet'], net.get('gw')
        if (net['name'] in net_list):
            raise BuildError("network %s is already defined" % net['name'])
        net_builder[net['name']] =  (net['subnet'], net.get('gw'))

if ( spec['Hosts']):
    print " building servers"
    for host in spec['Hosts']:
        print "building host ", host['name'] , host['image'], host['flavor'], host.get('net'), host.get('env')
        print "checking host name ", host['name']
        if (host['name'] in server_list):
            raise BuildError("host %s is already defined" % host['name'])
        print "checking host image ", host['image']
        image = nova.images.find(name=host['image'])
        print "checking host flavor ", host['flavor']
        image = nova.flavors.find(name=host['flavor'])

        for (name,ip) in host.get('net'):
            if (name not in net_builder):
                raise BuildError("host network %s not defined" % name)
