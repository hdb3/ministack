from neutronclient.v2_0 import client
import os
import traceback
from pprint import pprint


class Neutron:
    def __init__ (self, auth_url, credentials):
        self.neutron = client.Client( username = credentials['user'],
                                      password = credentials['password'],
                                      tenant_name = credentials['project'],
                                      auth_url = auth_url)
        self.networks = self.neutron.list_networks()['networks']
        # pprint(self.networks)
        self.net_by_name = {}
        for net in self.networks:
            self.net_by_name[net['name']] = net
        # pprint(self.net_by_name)
    
    def port_build(self,network_id, ip_address):
        body_value = {
            "port": {
            "admin_state_up": True,
            # "name": "port1",
            "network_id": network_id,
            "fixed_ips": [
                {
                    # "subnet_id": "a0304c3a-4f08-4c43-88af-d796509c97d2",
                    "ip_address": ip_address
                }
            ],
            }
        }
        response = self.neutron.create_port(body=body_value)
        # pprint(response)
        return response['port']['id']
    
    def net_delete(self,net_id):
        port_list = self.neutron.list_ports()
        for port in port_list['ports']:
            # pprint(port)
            if port['network_id'] == net_id:
                port_id = port['id']
                print "deleting port " , port_id
                self.neutron.delete_port(port_id)
        print "deleting net  " , net_id
        self.neutron.delete_network(net_id)
    
    def net_build(self,name,network,vlan,start,end,subnet,gw):

        def create_router(name,external_network_name):
            if external_network_name not in self.net_by_name:
                print "the referenced external network %s in virtual network %s does not exist " % (external_network_name,name)
                sys.exit(1)
            router = self.neutron.create_router(
                {
                   "router": {
                      "name" : name,
                      "external_gateway_info": {
                         "network_id": self.net_by_name[external_network_name]['id']
                      }
                   }
                })
            pprint(router)
            return router['router']['id']

        def add_interface_router(router_id,subnet_id):
            return self.neutron.add_interface_router( router_id,
                { "subnet_id" : subnet_id } )

        def net_template(name,network,vlan):
            if vlan == 0: # this is a pure virtual network, possibly with a NATed external network
                return  {
                    "network":
                        {
                        "name": name,
                        "admin_state_up": True,
                        "shared": True,
                        "router:external": False,
                        }
                }
            else:
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
                    "gateway_ip": gw,
                    "enable_dhcp": True,
                    "dns_nameservers": ["8.8.8.8"],
                    "host_routes": [ {"destination": "0.0.0.0/0", "nexthop": gw} ],
                    "name" : name,
                    "network_id" : network_id,
                    "allocation_pools" : [ { "start": start, "end": end } ]
                 } ]
            }
        try:
            net = net_template(name,network,vlan)
            net_response = self.neutron.create_network(body=net)
            # pprint(net_response)
            net_dict = net_response['network']
            network_id = net_dict['id']
            # print "Network %s created" % network_id
    
            subnet = subnet_template(name,network_id,start,end,subnet,gw)
    
            subnet_response = self.neutron.create_subnet(body=subnet)
            assert (len(subnet_response['subnets']) == 1)
            pprint(subnet_response)
            subnet_id = subnet_response['subnets'][0]['id']
            print "subnet ID is %s " % subnet_id

            if (network and vlan == 0): # virtual network, may want a router...
            # print "Created subnet %s" % subnet
                print "adding a router for network %s to external network %s" % (name,network)
                router_id = create_router(name,network)
                add_interface_router(router_id,subnet_id)
        except: # DANGEROUS! what exception am I actually trying to catch here?  not language errors!
            print(traceback.format_exc())
            return None
    
        print "Build completed"
    
        return network_id
