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

def port_build(network_id, ip_address):
    body_value = {
        "port": {
        "admin_state_up": True,
        "name": "port1",
        "network_id": network_id,
        "fixed_ips": [
            {
                # "subnet_id": "a0304c3a-4f08-4c43-88af-d796509c97d2",
                "ip_address": ip_address
            }
        ],
        }
    }
    response = neutron.create_port(body=body_value)
    # pprint(response)
    return response['port']['id']

def net_delete(net_id):
    port_list = neutron.list_ports()
    for port in port_list['ports']:
        # pprint(port)
        if port['network_id'] == net_id:
            port_id = port['id']
            print "deleting port " , port_id
            neutron.delete_port(port_id)
    print "deleting net  " , net_id
    neutron.delete_network(net_id)

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
