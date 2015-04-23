
spec = {
    'name' : "faulty template",
    'default network name' : "mgmt-nxt",
    'external network name' : "ext-net1",
    'keypair' : "dell5",
    'Networks' : [
        { 'name' : "lan1" , 'subnet' :" 192.168.1.0/24" , 'gw': "192.168.1.1" },
        { 'name' : "lan2" , 'subnet' :" 192.168.2.0/24" }
    ],
    'Hosts' : [
        { 'name' : "foo" , 'image' : "centos7" , 'flavor':"m1.large" , 'net' : [ ("lan1" , "192.168.1.1") ] , 'env' : ["role=client" , "target=bar"] },
        { 'name' : "bar" , 'image' : "centos7" , 'flavor':"m1.large" , 'net' : [ ("lan3" , "192.168.1.2") , ("lan2" , "192.168.2.2") ] , 'env' : ["role=middleware" , "target=baz"] },
        { 'name' : "baz" , 'image' : "centos7" , 'flavor':"m1.large" , 'net' : [ ("lan2" , "192.168.2.2") ] , 'env' : ["role=server"] }
    ]
}
