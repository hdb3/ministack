
spec = {
    'name' : "Mu's template",
    'default network name' : "demo-net3",
    'external network name' : "ext-net3",
    'keypair' : "dell4",
    'Networks' : [
        { 'name' : "lan201" , "start": "192.168.1.201", "end": "192.168.1.202", "subnet" :" 192.168.1.0/24", "vlan": 201 },
        { 'name' : "lan202" , "start": "192.168.1.202", "end": "192.168.1.203", "subnet" :" 192.168.1.0/24", "vlan": 202 }
    ],
    'Hosts' : [
        { 'name' : "h201" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan201" , "192.168.1.201") ] },
        { 'name' : "h202" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan202" , "192.168.1.202") ] },
    ]
}
