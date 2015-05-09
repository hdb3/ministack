
spec = {
    'name' : "Mu's template #2",
    'default network name' : "demo-net3",
    'external network name' : "ext-net3",
    'keypair' : "dell4",
    'Networks' : [
        { 'name' : "lan211" , "start": "192.168.1.211", "end": "192.168.1.212", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 211, "physical_network": "vlannet" },
        { 'name' : "lan212" , "start": "192.168.1.212", "end": "192.168.1.213", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 212, "physical_network": "vlannet" },
        { 'name' : "lan213" , "start": "192.168.1.213", "end": "192.168.1.214", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 213, "physical_network": "vlannet" },
        { 'name' : "lan214" , "start": "192.168.1.214", "end": "192.168.1.215", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 214, "physical_network": "vlannet" },
        { 'name' : "lan215" , "start": "192.168.1.215", "end": "192.168.1.216", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 215, "physical_network": "vlannet" },
        { 'name' : "lan216" , "start": "192.168.1.216", "end": "192.168.1.217", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 216, "physical_network": "vlannet" },
        { 'name' : "lan217" , "start": "192.168.1.217", "end": "192.168.1.218", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 217, "physical_network": "vlannet" },
        { 'name' : "lan218" , "start": "192.168.1.218", "end": "192.168.1.219", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 218, "physical_network": "vlannet" },
        { 'name' : "lan219" , "start": "192.168.1.219", "end": "192.168.1.221", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 219, "physical_network": "vlannet" },
        { 'name' : "lan220" , "start": "192.168.1.220", "end": "192.168.1.221", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1", "vlan": 220, "physical_network": "vlannet" },
    ],
    'Hosts' : [
        { 'name' : "h211" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan211" , "192.168.1.211") ] },
        { 'name' : "h212" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan212" , "192.168.1.212") ] },
        { 'name' : "h213" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan213" , "192.168.1.213") ] },
        { 'name' : "h214" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan214" , "192.168.1.214") ] },
        { 'name' : "h215" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan215" , "192.168.1.215") ] },
        { 'name' : "h216" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan216" , "192.168.1.216") ] },
        { 'name' : "h217" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan217" , "192.168.1.217") ] },
        { 'name' : "h218" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan218" , "192.168.1.218") ] },
        { 'name' : "h219" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan219" , "192.168.1.219") ] },
        { 'name' : "h220" , 'image' : "cirros" , 'flavor':"m1.small" , 'net' : [ ("lan220" , "192.168.1.220") ] },
    ]
}
