
spec = {
    'name' : "Mu's template #2",
    'default network name' : "demo-net3",
    'external network name' : "ext-net3",
    'keypair' : "dell4",
    'Networks' : [
        { 'name' : "lan201" , "start": "192.168.1.201", "end": "192.168.1.202", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 201, "physical_network": "vlannet" },
        { 'name' : "lan202" , "start": "192.168.1.202", "end": "192.168.1.203", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 202, "physical_network": "vlannet" },
        { 'name' : "lan203" , "start": "192.168.1.203", "end": "192.168.1.204", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 203, "physical_network": "vlannet" },
        { 'name' : "lan204" , "start": "192.168.1.204", "end": "192.168.1.205", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 204, "physical_network": "vlannet" },
        { 'name' : "lan205" , "start": "192.168.1.205", "end": "192.168.1.206", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 205, "physical_network": "vlannet" },
        { 'name' : "lan206" , "start": "192.168.1.206", "end": "192.168.1.207", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 206, "physical_network": "vlannet" },
        { 'name' : "lan207" , "start": "192.168.1.207", "end": "192.168.1.208", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 207, "physical_network": "vlannet" },
        { 'name' : "lan208" , "start": "192.168.1.208", "end": "192.168.1.209", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 208, "physical_network": "vlannet" },
        { 'name' : "lan209" , "start": "192.168.1.209", "end": "192.168.1.210", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 209, "physical_network": "vlannet" },
        { 'name' : "lan210" , "start": "192.168.1.210", "end": "192.168.1.211", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 210, "physical_network": "vlannet" },
    ],
    'Hosts' : [
        { 'name' : "h201" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan201" , "192.168.1.201") ] },
        { 'name' : "h202" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan202" , "192.168.1.202") ] },
        { 'name' : "h203" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan203" , "192.168.1.203") ] },
        { 'name' : "h204" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan204" , "192.168.1.204") ] },
        { 'name' : "h205" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan205" , "192.168.1.205") ] },
        { 'name' : "h206" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan206" , "192.168.1.206") ] },
        { 'name' : "h207" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan207" , "192.168.1.207") ] },
        { 'name' : "h208" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan208" , "192.168.1.208") ] },
        { 'name' : "h209" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan209" , "192.168.1.209") ] },
        { 'name' : "h210" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan210" , "192.168.1.210") ] },
    ]
}
