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
from socket import gethostbyname 
from os import environ as env
import os
import argparse
from pprint import pprint
import novaclient.client
from neutron import Neutron

spec_error = False

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--auth','-a', action='store_true')
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
    # print "using OpenStack auth credentials from spec file"
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

if args.auth:
    print "credentials string:\nexport OS_USERNAME=%s OS_PASSWORD=%s OS_TENANT_NAME=%s OS_AUTH_URL=%s" % (credentials['user'],credentials['password'],credentials['project'],auth_url)
    sys.exit(0)

config = {}
config['external_network_name'] = spec.get('external network name')
#config['external_network_name'] = get(spec['external network name']
config['dns'] = spec['dns']
neutron = Neutron(auth_url, credentials, config)
nova    = novaclient.client.Client("2",
                                   username = credentials['user'],
                                   api_key = credentials['password'],
                                   project_id = credentials['project'],
                                   auth_url = auth_url)

servers = nova.servers.list()
server_list = {}
for server in servers:
    server_list[server.name] = (server.id,server.status)

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

# the net_list somewhat duplicates functionality in the neutron library (net_by_name)
# and should probably be removed
# however, the possibility of non-unique net names should be considered
# before completly removing visibility of net IDs in this code...
net_list = {}
for net in neutron.networks:
  net_list[net['name']] = net['id']

def name_to_address(name):
    global spec_error

    if "*" == name:
        return "*"

    try:
        address = gethostbyname(name)
    except:
        print "Unexpected error looking up hostname '%s':" % name, sys.exc_info()[0]
        spec_error = True
        return name

    if address:
        return address

    print stderr,"host lookup failed for '%s'" % name
    spec_error = True
    return name

def check_keypair(name):
    try:
        return not ( nova.keypairs.get(name).deleted )
    except novaclient.exceptions.NotFound:
        return False
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


if (not args.delete):
    if check_keypair(spec['keypair']):
        pass
    else:
        print "checking keypair failed"
        sys.exit(1)

net_builder = {}
host_builder = {}
router_needed = {}

if (args.resume or args.suspend):
    pass
elif ( not spec['Networks']):
    print "warning: no Networks in spec file"
    # sys.exit(1)
else:
    for net in spec['Networks']:
        net_name = net['name']
        if (not args.delete):
            if (net_name in net_list):
                if (args.dryrun or build):
                    spec_error = True
                    print "Build warning - network %s is already defined" % net_name
                else:
                    print "network %s exists" % net_name
            else:
                net_builder[net_name] =  net
        elif (args.delete > 1):
            if (net_name in net_list):
                net_builder[net_name] =  net
            else:
                print "Can't delete non-existent network %s" % net_name

if ( not spec['Hosts']):
    print "Warning - no hosts section in spec file"
else:
    print "processing servers"
    for host in spec['Hosts']:
        if (build or args.dryrun or args.complete):
            print "building host ", host['name'] , host['image'], host['flavor'], host.get('net'), host.get('env')
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
                try:
                    for net_entry in host.get('net'):
                    # a host network entry defines the network to be used, the assigned IP, and an optional floating IP
                    # the network name is the actual name used in openstack, and must either be defined in the spec file or already exist
                    # there must be a (local) IP (OpenStack insists...) but it can be wildcarded, in which case one will be selected from the pool
                    # the optional third field is for a floating IP - this can be either a domain name or an IP
                    # in either case it will be assigned from the external network range which is defined in the spec file
                    # the first (local) IP may also be a hostname, which is most useful for cases where the attached network is directly routable
                        ip = None
                        fip_id = None
                        if isinstance(net_entry,tuple):
                            name = net_entry[0]
                            if len(net_entry) > 1:
                                ip = name_to_address(net_entry[1])
                            if len(net_entry) > 2:
                                fip = name_to_address(net_entry[2])
                                fip_id = neutron.get_floatingip(config['external_network_name'],fip,args.dryrun)
                        elif isinstance(net_entry,basestring):
                            name = net_entry
                        else:
                            # if net_entry is neither a string or a tuple then I am confused....
                            print "Why me....?"
                            sys.exit(1)
                        if (name in net_builder or name in net_list):
                            nets.append((name,ip,fip_id))
                        else:
                            print "Build warning - host network %s not defined" % name
                            spec_error = not (args.complete)

                    host_builder[host['name']] = (image,flavor,nets)

                except:
                    print "this is an unexpected exception!"
                    print(traceback.format_exc())
                    sys.exit(1)
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
    for net in net_builder.values():
        net_name = net['name']
        if (args.delete):
            neutron.net_delete(net_list[net_name])
        else:
            net_id = neutron.net_build(net)
            if (net_id):
                net_list[net_name] = net_id
            else:
                print "error: failed to build network %s" % net_name
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
            for (name,ip,fip_id) in ns:
                id=net_list[name]
                port_id = neutron.port_build(id,ip)
                nics.append({'port-id': port_id})
                if (fip_id): # floating IP requested
                    neutron.floatingip_bind(port_id,fip_id)
            instance = nova.servers.create(name=k, image=i, flavor=f, key_name=spec['keypair'], nics=nics, config_drive=True)


if (args.delete > 1):
    process_servers()
    process_networks()
elif (build or args.complete):
    process_networks()
    process_servers()
else:
    process_servers()
