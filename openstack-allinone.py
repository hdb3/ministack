
spec = {
    'name' : "a 4-node openstack cluster",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "os-provider" , "subnet" :" 172.16.1.0/24","start": "172.16.1.3", "end": "172.16.1.254", "gateway": "172.16.1.1" },
    ],
    'Hosts' : [
        { 'name' : "os-allinone"    , 'image' : "centos1602" , 'flavor':"m1.large" , 'net' : [ ("routed-net" , "os-allinone"),  ("os-provider","*") ] },
    ]
}
