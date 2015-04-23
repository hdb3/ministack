import os
from pprint import pprint
from neutronclient.v2_0 import client

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
    pprint.pprint(netw['networks'])

print dir(neutron)
print "\n********************\n"
networks = neutron.list_networks()['networks']
for net in neutron.list_networks()['networks']:
  print net['name'], net['id']
# pprint(networks)
# (k,v) = neutron.list_networks().popitem()
# pprint(k)
# pprint(v)
# pprint (neutron.networks)
