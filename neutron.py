#refer to http://developer.openstack.org/api-ref-networking-v2-ext.html for details of the API...
from neutronclient.v2_0 import client
import os
import sys
import traceback
from keystoneclient.v2_0 import client as keystone_client
from pprint import pprint


class Neutron:
    def __init__ (self, auth_url, credentials, config):
        self.neutron = client.Client( username = credentials['user'],
                                      password = credentials['password'],
                                      tenant_name = credentials['project'],
                                      auth_url = auth_url)
        self.networks = self.neutron.list_networks()['networks']
        self.floating_ips = self.neutron.list_floatingips()['floatingips']
        self.net_by_name = {}
        for net in self.networks:
            self.net_by_name[net['name']] = net
        self.external_network_name = config['external_network_name']
        self.dns = config['dns']
        self.external_network_id = self.net_by_name[self.external_network_name]['id']

        keystone = keystone_client.Client( username = credentials['user'],
                                  password = credentials['password'],
                                  tenant_name = credentials['project'],
                                  auth_url = auth_url)

        # tenants = keystone.tenants.list()
        # for tenant in tenants:
        for tenant in keystone.tenants.list():
          if tenant.name == credentials['project']:
              # print "found my project! %s, ID=%s" % (credentials['project'], tenant.id)
              self.tenant_id = tenant.id
              break

#   users = keystone.users.list()

#   for user in users:
#     if user.name == credentials['user']:
#         print "found my user! %s, ID=%s" % (credentials['user'], user.id)
#         # pprint(user)
#         if user.tenantId == my_tenant_id:
#             print "and my tenant ID agrees with the one given to me in the environment or spec file..."
#         else:
#             print "but my tenant ID does not agree with the one given to me in the environment or spec file...",
#             print " from user record: %s" % user.tenantId,
#             print " from tenant record: %s" % my_tenant_id
    
    def floatingip_bind(self, port_id, floatingip_id):
        try:
            self.neutron.update_floatingip(floatingip_id, {'floatingip' : { 'port_id' : port_id }})
        except:
            print "floating IP bind unexpectedly failed"
            print(traceback.format_exc())
            sys.exit(1)

    def get_floatingip(self,external_net_name,floatingip,dryrun):
        net_id = self.net_by_name[external_net_name]['id']
        if "*" == floatingip: # any address will do....
            print "non specific floating IP requested...."
            for f in self.floating_ips:
               if net_id == f["floating_network_id"] and not f['port_id'] and f['tenant_id'] == self.tenant_id:
                   print "assigning existing floating IP address %s, ID:%s" % (floatingip,f['floating_ip_address'])
                   return f['id']
            # no existing float matches - need to assign a new floating IP
            if dryrun:
                print "no existing floating IP available - not creating one because this is a dryrun"
                return None
            else:
                response = self.neutron.create_floatingip({ 'floating_network_id' : net_id })
                pprint(response)
                return response['id']

        # we were asked for a specific floating IP address.....
        for f in self.floating_ips:
           if net_id == f["floating_network_id"] and floatingip == f["floating_ip_address"]:
               if f['port_id']: # give up - the IP address exists and is in use
                   print "error - floating IP address %s is already in use for port %s" % (floatingip,f['port_id'])
                   return None
               elif f['tenant_id'] != self.tenant_id: # give up - the IP address exists and is owned by someone else
                   print "error - floating IP address %s is owned by another project: %s" % (floatingip,f['tenant_id'])
                   return None
               else:
                   print "assigning existing floating IP address %s, ID:%s" % (floatingip,f['id'])
                   return f['id']
        # no existing float matches - need to assign a new floating IP
        if dryrun:
            print "no existing floating IP available - not creating one because this is a dryrun"
            return None
        else:
            response = self.neutron.create_floatingip({ 'floatingip' : { 'floating_network_id' : net_id, 'floating_ip_address' : floatingip }})
            pprint(reponse)
            return response['id']

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
                # can't delete the port directly, but removing the interface from the associated router also removes this kind of port
                    self.neutron.remove_interface_router( port['device_id'], body={'port_id' : port_id})
                    print "deleting router " , port['device_id']
                    self.neutron.delete_router( port['device_id'])
                else:
                    self.neutron.delete_port(port_id)
        print "deleting net  " , net_id
        self.neutron.delete_network(net_id)
    
    def net_build(self,name,network,vlan,start,end,subnet,gw,router_needed):

        def create_router(name,external_network_id):
            router = self.neutron.create_router(
                {
                   "router": {
                      "name" : name,
                      "external_gateway_info": {
                         "network_id": external_network_id
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
                    "dns_nameservers": [self.dns],
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

            if router_needed:
                if not vlan == 0:
                    print "*** Warning: adding router for VLAN network - is this really wanted!!!!?"
                print "adding a router for network %s to external network" % name
                router_id = create_router(name,self.external_network_id)
                add_interface_router(router_id,subnet_id)
        except: # DANGEROUS! what exception am I actually trying to catch here?  not language errors!
            print(traceback.format_exc())
            return None
    
        print "Build completed"
    
        return network_id
