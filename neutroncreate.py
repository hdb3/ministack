from neutronclient.v2_0 import client
import os
from pprint import pprint

def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


credentials = get_credentials()
neutron = client.Client(**credentials)

def net_template(name,network,vlan):
    return  {
        "network":
            {
            "name": name,
            "admin_state_up": True,
            "shared": True,
            "router:external": False,
            "provider:network_type": "vlan",
            "provider:segmentation_id": vlan,
            "provider:physical_network": network
        }
    }

def subnet_template(name,network_id,start,end,subnet,gw):
    return {
    "subnets": [
        {
            "name": name,
            "cidr": subnet,
            "ip_version": 4,
            "gateway_ip": None,
            "enable_dhcp": True,
            "dns_nameservers": ["8.8.8.8"],
            "host_routes": [ {"destination": "0.0.0.0/0", "nexthop": gw} ],
            "name" : name,
            "network_id" : network_id,
            "allocation_pools" : [ { "start": start, "end": end } ]
         } ]
    }

def net_build(name,network,vlan,start,end,subnet,gw):
    try:
        net = net_template(name,network,vlan)
        net_response = neutron.create_network(body=net)
        net_dict = net_response['network']
        network_id = net_dict['id']
        # print "Network %s created" % network_id

        subnet = subnet_template(name,network_id,start,end,subnet,gw)

        subnet_response = neutron.create_subnet(body=subnet)
        # print "Created subnet %s" % subnet
    except:
        return None

    print "Build completed"

    return network_id

if __name__ == "__main__":
    nets=[]
    nets.append(net_build("net201","vlannet",201,"192.168.1.1","192.168.1.2","192.168.1.0/24","192.168.1.1"))
    nets.append(net_build("net202","vlannet",202,"192.168.1.2","192.168.1.3","192.168.1.0/24","192.168.1.1"))
    nets.append(net_build("net203","vlannet",203,"192.168.1.3","192.168.1.4","192.168.1.0/24","192.168.1.1"))
    pprint (nets)
