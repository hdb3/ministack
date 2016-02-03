
spec = {
    'name' : "switch 1 VLANs",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    # 'credentials' : { 'user' : "admin", 'password' : "admin", 'project' : "admin" },
    # NOTE: network start/end range -
    #       a) must not include the gateway IP
    #       b) when assigning host IPs remember taht a DHCP server will be allocated from the range as well as the hosts
    #          Probably on the first or second available IP in the range....
    'keypair' : "x220",
    'Networks' : [
        { 'name' : "net4001" , "start": "192.168.99.200", "end": "192.168.99.254", "subnet" :" 192.168.99.0/24", "gateway": "192.168.99.1", "vlan": 4001, "physical_network": "vlannet" },
        { 'name' : "net4002" , "start": "192.168.99.200", "end": "192.168.99.254", "subnet" :" 192.168.99.0/24", "gateway": "192.168.99.1", "vlan": 4002, "physical_network": "vlannet" },
        { 'name' : "net4000-mgmt" , "start": "192.168.1.200", "end": "192.168.1.254", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1" }
    ],
    'Hosts' : [
        { 'name' : "h4001" , 'image' : "cirros" , 'flavor':"m1.tiny" , 'net' : [ ("net4000-mgmt" , "*", "*") , ("net4001" , "192.168.99.201" ) ] },
        { 'name' : "h4002" , 'image' : "cirros" , 'flavor':"m1.tiny" , 'net' : [ ("net4000-mgmt" , "*", "*") , ("net4002" , "192.168.99.202" ) ] }
    ]
}
