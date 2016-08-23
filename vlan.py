
spec = {
    'name' : "simple 2 host VLAN-mux topology",
    'external network name' : "exnet3",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'keypair' : "openstack_rsa",
    'Networks' : [
        { 'name' : "lan201" , "start": "192.168.1.201", "end": "192.168.1.202", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 201, "physical_network": "vlannet" },
        { 'name' : "lan202" , "start": "192.168.1.202", "end": "192.168.1.203", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 202, "physical_network": "vlannet" },
    ],
    'Hosts' : [
        { 'name' : "h201" , 'image' : "ubuntu-16.04" , 'flavor':"m1.small" , 'net' : [ ("routed-net" , "h201"), ("lan201" , "192.168.1.201") ] },
        { 'name' : "h202" , 'image' : "ubuntu-16.04" , 'flavor':"m1.small" , 'net' : [ ("routed-net" , "h202"), ("lan202" , "192.168.1.202") ] },
    ]
}
