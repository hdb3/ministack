
spec = {
    'name' : "Mu's template",
    'default network name' : "demo-net3",
    'external network name' : "ext-net3",
    'keypair' : "dell4",
    'Networks' : [
#        { 'name' : "lan200" , "start": "192.168.1.200", "end": "192.168.1.201", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 200, "physical_network": "vlannet" },
        { 'name' : "lan201" , "start": "192.168.1.201", "end": "192.168.1.202", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 201, "physical_network": "vlannet" },
        { 'name' : "lan202" , "start": "192.168.1.202", "end": "192.168.1.203", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 202, "physical_network": "vlannet" }
    ],
    'Hosts' : [
#        { 'name' : "h200" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan200" , "192.168.1.200") ] },
        { 'name' : "h201" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan201" , "192.168.1.201") ] },
        { 'name' : "h202" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan202" , "192.168.1.202") ] },
    ]
}
