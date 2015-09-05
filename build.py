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
# from neutronclient.v2_0 import client
import novaclient.client
# from neutroncreate import net_build,net_delete,port_build
from neutron import Neutron

spec_error = False

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--dryrun','-n', action='store_true')
group.add_argument('--build','-b', action='store_true')
group.add_argument('--delete', '-d', action='count')
group.add_argument('--suspend', '-s', action='store_true')
group.add_argument('--resume', '-r', action='store_true')
group.add_argument('--complete','-c', action='store_true')
parser.add_argument('specfile')
args=parser.parse_args()
specfile=args.specfile

# build is the default action
build = not (args.resume or args.suspend or args.complete or args.dryrun or args.delete)

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

if spec['credentials'] and spec['controller']:
    print "using OpenStack auth credentials from spec file"
    credentials = spec['credentials']
    auth_url = "http://" + spec['controller'] + ":35357/v2.0"
elif (os.environ['OS_USERNAME'] and os.environ['OS_PASSWORD'] and os.environ['OS_AUTH_URL'] and os.environ['OS_TENANT_NAME']):
    print "using OpenStack auth credentials from environment"
    credentials = { 'user' : os.environ['OS_USERNAME'],
                    'password' : os.environ['OS_PASSWORD'],
                    'project' : os.environ['OS_TENANT_NAME'] }
    auth_url = os.environ['OS_AUTH_URL']
else:
    print "Can't find OpenStack auth credentials in environment or spec file, giving up..."
    sys.exit(1)

# neutron = client.Client( username = credentials['user'],
#                         password = credentials['password'],
#                         tenant_name = credentials['project'],
#                         auth_url = auth_url)
neutron = Neutron(auth_url, credentials)
nova    = novaclient.client.Client("2",
                                   username = credentials['user'],
                                   api_key = credentials['password'],
                                   project_id = credentials['project'],
                                   auth_url = auth_url)

servers = nova.servers.list()
server_list = {}
for server in servers:
    server_list[server.name] = (server.id,server.status)
    # print "server %s %s %s" % (server.name,server.id,server.status)

def server_suspend(name):
    for s in servers:
        if s.name == name:
            (id,status) = server_list[name]
            if (status == 'ACTIVE'):
                response = nova.servers.suspend(s)
                print "suspend %s" % name, response
            else:
                print "Can't suspend server %s  in state %s  "  % (name,status)

def server_resume(name):
    for s in servers:
        if s.name == name:
            response = nova.servers.resume(s)
            print "resume %s" % name, response

def server_delete(name):
    for s in servers:
        if s.name == name:
            response = nova.servers.delete(s)
            print "delete %s" % name, response

net_list = {}
for net in neutron.networks:
  net_list[net['name']] = net['id']

def check_keypair(name):
    try:
        return not ( nova.keypairs.get(name).deleted )
    except novaclient.exceptions.NotFound:
        return False
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

if (not args.delete):
    print "Checking global parameters"

    print "checking keypair" , spec['keypair'],
    if check_keypair(spec['keypair']):
        print "OK"
    else:
        print "failed"
        sys.exit(1)

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

if (args.resume or args.suspend):
    pass
elif ( not spec['Networks']):
    print "Error: no Networks in spec file"
    sys.exit(1)
else:
    print "processing networks"
    for net in spec['Networks']:
        if 'vlan' not in net:
            net['vlan'] = 0
        if (not args.delete):
            print "building network ", net['name'] , net['start'], net['end'], net['subnet'], net['gateway'], net['vlan'], net['physical_network']
            if (net['name'] in net_list):
                if (args.dryrun or args.build):
                    spec_error = True
                    print "Build Error - network %s is already defined" % net['name']
                else:
                    print "network %s exists" % net['name']
            else:
                net_builder[net['name']] =  (net['start'], net['end'], net['subnet'], net['gateway'], net['vlan'],net['physical_network'])
        elif (args.delete > 1):
            if (net['name'] in net_list):
                print "Will delete network %s" % net['name']
                net_builder[net['name']] =  (net['start'], net['end'], net['subnet'], net['gateway'], net['vlan'],net['physical_network'])
            else:
                print "Can't delete non-existent network %s" % net['name']

if ( not spec['Hosts']):
    print "Warning - no hosts section in spec file"
else:
    print "processing servers"
    for host in spec['Hosts']:
        if (args.build or args.dryrun or args.complete):
            print "building host ", host['name'] , host['image'], host['flavor'], host.get('net'), host.get('env')
            # print "checking host name ", host['name']
            if (host['name'] in server_list):
                if (args.complete):
                    print "host %s exists" % host['name']
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
                    if (name not in net_builder and name not in net_list):
                        if (args.complete):
                            print "Build warning - host network %s not defined" % name
                        else:
                            spec_error = True
                            print "Build Error - host network %s not defined" % name
                    else:
                        nets.append((name,ip))
                host_builder[host['name']] = (image,flavor,nets)
        else:
            if (host['name'] in server_list):
                print "processing host %s" % host['name']
                host_builder[host['name']] = None
            else:
                print "not processing host %s (server does not exist)" % host['name']

if (spec_error):
    print "not building cluster due to spec errors"
    sys.exit(1)

if (args.dryrun):
    print "dryrun only - not processing cluster"
    sys.exit(0)


def process_networks():
    print "processing networks"
    if (args.delete):
        for name in net_builder.keys():
            # neutron.delete_network(net_list[name])
            neutron.net_delete(net_list[name])
    else:
        for name,(start,end,subnet,gw,vlan,phynet) in net_builder.items():
            print "net %s : (%s,%s,%s,%s,%d,%s)" % (name,start,end,subnet,gw,vlan,phynet)
            net_id = neutron.net_build(name,phynet,vlan,start,end,subnet,gw)
            if (net_id):
                net_list[name] = net_id
            else:
                print "error: failed to build network %s" % name
                sys.exit(1)


def process_servers():
    print "processing servers"
    if (args.delete):
        for k in host_builder.keys():
            server_delete(k)
    elif (args.suspend):
        for k in host_builder.keys():
            server_suspend(k)
    elif (args.resume):
        for k in host_builder.keys():
            server_resume(k)
    else:
        for k,(i,f,ns) in host_builder.items():
            print "host %s : (%s,%s)" % (k,i,f)
            nics=[]
            for (name,ip) in ns:
                id=net_list[name]
                # nics.append({'net-id': id})
                port_id = neutron.port_build(id,ip)
                nics.append({'port-id': port_id})
            # pprint ({ 'name':k, 'image':i, 'flavor':f, 'key_name':spec['keypair'], 'nics':nics})
            instance = nova.servers.create(name=k, image=i, flavor=f, key_name=spec['keypair'], nics=nics, config_drive=True)


if (args.delete > 1):
    process_servers()
    process_networks()
elif (args.build or args.complete):
    process_networks()
    process_servers()
else:
    process_servers()
