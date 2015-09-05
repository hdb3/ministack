from neutronclient.v2_0 import client
import os
import sys
import traceback
# from pprint import pprint


class Neutron:
    def __init__ (self, auth_url, credentials):
        self.neutron = client.Client( username = credentials['user'],
                                      password = credentials['password'],
                                      tenant_name = credentials['project'],
                                      auth_url = auth_url)
        self.networks = self.neutron.list_networks()['networks']
        self.net_by_name = {}
        for net in self.networks:
            self.net_by_name[net['name']] = net
    
    def port_build(self,network_id, ip_address):
        body_value = {
            "port": {
            "admin_state_up": True,
            "network_id": network_id,
            "fixed_ips": [
                {
                    "ip_address": ip_address
                }
            ],
            }
        }
        response = self.neutron.create_port(body=body_value)
        return response['port']['id']
    
    def net_delete(self,net_id):
    # deleting a network requires removal of child objects like ports and routers
    # removing a router may require prior removal of interfaces
    # we search routers for 
        port_list = self.neutron.list_ports()
        for port in port_list['ports']:
            if port['network_id'] == net_id:
                port_id = port['id']
                print "deleting port " , port_id
                if port['device_owner'] == "network:router_interface":
                    # print "hmmm, %s is an awkward port, and we should probably find an associated router to bork" % port_id
                    # print "the network ID in question is %s" % port['network_id']
                    # print "the device ID (router) in question is %s" % port['device_id']
                    self.neutron.remove_interface_router( port['device_id'], body={'port_id' : port_id})
                    print "deleting router " , port['device_id']
                    self.neutron.delete_router( port['device_id'])
                else:
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
            net_dict = net_response['network']
            network_id = net_dict['id']
    
            subnet = subnet_template(name,network_id,start,end,subnet,gw)
    
            subnet_response = self.neutron.create_subnet(body=subnet)
            assert (len(subnet_response['subnets']) == 1)
            subnet_id = subnet_response['subnets'][0]['id']
            print "subnet ID is %s " % subnet_id

            if (network and vlan == 0): # virtual network, may want a router...
                print "adding a router for network %s to external network %s" % (name,network)
                router_id = create_router(name,network)
                add_interface_router(router_id,subnet_id)
        except: # DANGEROUS! what exception am I actually trying to catch here?  not language errors!
            print(traceback.format_exc())
            return None
    
        print "Build completed"
    
        return network_id
