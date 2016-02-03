
spec = {
    'name' : "RYU template #1",
    'default network name' : "demo-net3",
    'external network name' : "ext-net3",
    'keypair' : "openstack_rsa",
    'Networks' : [
        { 'name' : "lan201" , "start": "192.168.1.200", "end": "192.168.1.210", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 201, "physical_network": "vlannet" },
        { 'name' : "lan202" , "start": "192.168.1.200", "end": "192.168.1.210", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 202, "physical_network": "vlannet" },
    ],
    'Hosts' : [
        { 'name' : "h201" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan201" , "192.168.1.201") ] },
        { 'name' : "h202" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan202" , "192.168.1.202") ] },
    ]
}
