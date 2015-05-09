#!/usr/bin/python
#
# build.py
#
# chain nova and neuton service requests to build predefined compute topologies
#
# topology is defined in python language 'spec' files
#
# by default the program will build the topology requested form a clean slate,
# but give the correct option (-c) it will also attempt to complete a build when some elements already exist, e.g. networks or compute instances
# Or, if option -d is given it will attempt to delete any VMs
# Of option -d is given twice it will also attempt to remove networks named in the spec file
# 
# before commencing work the program will make some basic checks on the spec file,
# e.g. checking that the named keypairs, flavors and images exist
#

##



import time
import sys
import traceback
from os import environ as env
import os
import argparse
from pprint import pprint
from neutronclient.v2_0 import client
import novaclient.client
from neutroncreate import net_build

spec_error = False

def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

parser = argparse.ArgumentParser()
parser.add_argument('--complete','-c', action='store_true')
parser.add_argument('--dryrun','-n', action='store_true')
parser.add_argument('--delete', '-d', action='count')
parser.add_argument('specfile')
args=parser.parse_args()
specfile=args.specfile
print "the spec file name is %s" % specfile


if ( not os.access(specfile,os.R_OK)):
    print "spec file not readable"
    sys.exit(1)

name,extension = os.path.splitext(specfile)
if ( extension and extension != ".py"):
    print "spec file not a python script"
    sys.exit(1)

try:
    _imp = __import__(name)
    spec = _imp.spec
    print "reading template: %s" % spec['name']
except:
    print "couldn't read the spec file '%s'" % specfile
    sys.exit(1)

credentials = get_credentials()
neutron = client.Client(**credentials)

nova = novaclient.client.Client("1.1", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                # region_name=env['OS_REGION_NAME']
                                )

server_list = {}
net_list = {}

for server in nova.servers.list():
    # print dir(server)
    # print server.name , server.id
    server_list[server.name] = server.id

#pprint(server_list)
#sys.exit(0)

for net in neutron.list_networks()['networks']:
  # print net['name'], net['id']
  net_list[net['name']] = net['id']


def check_keypair(name):
    try:
        return not ( nova.keypairs.get(name).deleted )
    except novaclient.exceptions.NotFound:
        return False
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

print "Checking global parameters"

print "checking keypair" , spec['keypair']
print check_keypair(spec['keypair'])

try:
    print "checking default network name" , spec['default network name']
    default_net = nova.networks.find(label=spec['default network name'])
    print "checking external network name" , spec['external network name']
    external_net = nova.networks.find(label=spec['external network name'])
except novaclient.exceptions.NotFound:
    print "Not found: " , sys.exc_value
    spec_error = True
except:
    traceback.print_exc()
    print "Unexpected error:", sys.exc_info()[0]
    sys.exit(1)

net_builder = {}
host_builder = {}

if ( spec['Networks']):
    print " building networks"
    for net in spec['Networks']:
        print "building network ", net['name'] , net['start'], net['end'], net['subnet'], net['gateway'], net['vlan'], net['physical_network']
        if (net['name'] in net_list):
            if (args.complete):
                print "Build warning - network %s is already defined" % net['name']
            else:
                spec_error = True
                print "Build Error - network %s is already defined" % net['name']
        else:
            net_builder[net['name']] =  (net['start'], net['end'], net['subnet'], net['gateway'], net['vlan'],net['physical_network'])

if ( spec['Hosts']):
    print " building servers"
    for host in spec['Hosts']:
        print "building host ", host['name'] , host['image'], host['flavor'], host.get('net'), host.get('env')
        print "checking host name ", host['name']
        if (host['name'] in server_list):
            if (args.complete):
                print "Build warning - host %s is already defined" % host['name']
            else:
                spec_error = True
                print "Build Error - host %s is already defined" % host['name']
        else:
            print "checking host image ", host['image']
            image = nova.images.find(name=host['image'])
            print "checking host flavor ", host['flavor']
            flavor = nova.flavors.find(name=host['flavor'])

            nets = []
            for (name,ip) in host.get('net'):
                if (name not in net_builder):
                    if (args.complete):
                        print "Build warning - host network %s not defined" % name
                    else:
                        spec_error = True
                        print "Build Error - host network %s not defined" % name
                else:
                    nets.append((name,ip))
            host_builder[host['name']] = (image,flavor,nets)

if (spec_error):
    print "not building cluster due to spec errors"
    sys.exit(1)

if (args.dryrun):
    print "dryrun only - not building cluster"
    sys.exit(0)


print "building networks"
for name,(start,end,subnet,gw,vlan,phynet) in net_builder.items():
    print "net %s : (%s,%s,%s,%s,%d,%s)" % (name,start,end,subnet,gw,vlan,phynet)
    net_id = net_build(name,phynet,vlan,start,end,subnet,gw)
    if (net_id):
        net_list[name] = net_id
    else:
        print "error: failed to build network %s" % name


print "building servers"
for k,(i,f,ns) in host_builder.items():
    print "host %s : (%s,%s)" % (k,i,f)
    nics=[]
    for (name,ip) in ns:
        id=net_list[name]
        nics.append({'net-id': id})
    pprint ({ 'name':k, 'image':i, 'flavor':f, 'key_name':spec['keypair'], 'nics':nics})
    instance = nova.servers.create(name=k, image=i, flavor=f, key_name=spec['keypair'], nics=nics)
