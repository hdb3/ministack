#refer to http://developer.openstack.org/api-ref-networking-v2-ext.html for details of the API...
from neutronclient.v2_0 import client
from neutronclient.common.exceptions import PortNotFoundClient
import os
import sys
import ipaddress # note - this requires the py2-ipaddress module!
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
        self.floating_ips = self.neutron.list_floatingips()['floatingips'] # a list of 'floatingip' dictionary objects is returned...
        self.net_by_name = {}
        for net in self.networks:
            self.net_by_name[net['name']] = net
        self.external_network_name = config['external_network_name']
        self.dns = config['dns']
        if self.external_network_name:
            self.external_network_id = self.net_by_name[self.external_network_name]['id']

        keystone = keystone_client.Client( username = credentials['user'],
                                  password = credentials['password'],
                                  tenant_name = credentials['project'],
                                  auth_url = auth_url)

        for tenant in keystone.tenants.list():
          if tenant.name == credentials['project']:
              self.tenant_id = tenant.id
              break
        if not hasattr(self,'tenant_id'):
            print "Could not find tenant  (_project_!) '%s' in Keystone directory\n" % credentials['project']
            sys.exit(1)

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
                   self.floating_ips.remove(f)
                   return f['id']
            # no existing float matches - need to assign a new floating IP
            if dryrun:
                print "no existing floating IP available - not creating one because this is a dryrun"
                return None
            else:
                response = self.neutron.create_floatingip({'floatingip': { 'floating_network_id' : net_id } })
                # pprint(response)
                return response['floatingip']['id']

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
            return response['floatingip']['id']

    def port_build(self,network_id, ip_address):
        body_value = {
            "port": {
            "admin_state_up": True,
            "network_id": network_id,
            }
        }
        if ip_address and not ("*" == ip_address):
            try:
                tmp = ipaddress.IPv4Address(unicode(ip_address)) # just using this to validate the IP address.....
                body_value['port']['fixed_ips'] = [ { "ip_address": ip_address } ]
            except ipaddress.AddressValueError:
                print "Warning - invalid IP address specified: %s " % ip_address
                pass
        response = self.neutron.create_port(body=body_value)
        return response['port']['id']
    
    def net_delete(self,net_id):
    # deleting a network requires removal of child objects like ports and routers
    # removing a router may require prior removal of interfaces
    # we search routers for 
        port_list = self.neutron.list_ports(network_id=net_id)['ports']
        repeat_flag = False
        # this is an endless loop if the ports can't be deleted!
        # hopefully however the loop never actually happens
        # most of the problems are probably due
        while len(port_list) > 0 :
            for port in port_list:
                if port['device_owner'] != "network:router_interface":
                    port_id = port['id']
                    if repeat_flag:
                        print "port delete retry: %s" % port_id
                    try: 
                        self.neutron.delete_port(port_id)
                    except PortNotFoundClient:
                        pass # we don't really care if the port has gone away already!
            port_list = self.neutron.list_ports(network_id=net_id)['ports']
            for port in port_list:
                if port['device_owner'] == "network:router_interface":
                    port_id = port['id']
                    if repeat_flag:
                        print "router port delete retry: %s" % port_id
                    self.neutron.remove_interface_router( port['device_id'], body={'port_id' : port_id})
                    self.neutron.delete_router( port['device_id'])
            port_list = self.neutron.list_ports(network_id=net_id)['ports']
            if len(port_list) > 0 :
                print "retrying some port delete operations!"
                repeat_flag = True
        print "deleting net  " , net_id
        self.neutron.delete_network(net_id)
    
    def net_build(self,net):

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

        def net_template(name):
                return  {
                        "name": name,
                        "admin_state_up": True,
                        "shared": False,
                        "router:external": False,
                }
        
        def subnet_template(name,network_id,subnet):
            return {
                    "name": name,
                    "cidr": subnet,
                    "ip_version": 4,
                    "gateway_ip": None,
                    "enable_dhcp": True,
                    "name" : name,
                    "network_id" : network_id,
                    # "dns_nameservers" : [], # unfortunately, even if a given interface has no gateway or DNS servers, dhclient will still wipeout a previous DNS name server
                                              # so it is important to always send the one you want to use
                                              # there is a different question, which is why dnsmasq does not correctly server DNS when contaced directly on these virtual interfaces...
                    "dns_nameservers" : [self.dns],
            }

        # unpack the mandatory network fields....
        name = net['name']
        subnet = net['subnet']

        net_request = net_template(name)
        if 'vlan' in net:
            net_request['provider:network_type'] = "vlan"
            net_request['provider:segmentation_id'] = net['vlan']
        if 'network' in net:
            net_request['provider:physical_network'] = net['network']
        elif 'physical_network' in net:
            net_request['provider:physical_network'] = net['physical_network']
        net_response = self.neutron.create_network(body={ "network" : net_request })['network']
        network_id = net_response['id']
    
        subnet_request = subnet_template(name,network_id,subnet)
        if 'vlan' in net:
            subnet_request['enable_dhcp'] = False
        if 'gateway' in net:
            subnet_request['gateway_ip'] = net['gateway']
            # subnet_request['dns_nameservers'] = [self.dns] # see abovce comment - always need this so don't bother doing it here too
            subnet_request['host_routes'] = [ {'destination': "0.0.0.0/0", 'nexthop': net['gateway']} ]
        if 'start' in net and 'end' in net:
            subnet_request['allocation_pools'] = [ { 'start': net['start'], 'end': net['end'] } ]
    
        subnet_response = self.neutron.create_subnet(body={"subnets": [subnet_request]})
        assert (len(subnet_response['subnets']) == 1)
        subnet_id = subnet_response['subnets'][0]['id']

        if 'gateway' in net:
            if 'vlan' in net:
                print "*** Error: not adding router for VLAN network - is this really wanted!!!!?"
            elif self.external_network_name:
                print "adding a router for network %s to external network" % name
                router_id = create_router(name,self.external_network_id)
                add_interface_router(router_id,subnet_id)
            else:
                print "Not creating router for external network because no external network is defined"
                print "The network will still be created - to suppress this message remove the gateway from the network definitiion"
    
        print "Network build completed"
    
        return network_id
