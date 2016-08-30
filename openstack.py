
spec = {
    'name' : "a 4-node openstack cluster",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "os-dataplane" , "subnet" :" 172.16.0.0/24" },
        { 'name' : "os-provider" , "subnet" :" 172.16.1.0/24","start": "172.16.1.3", "end": "172.16.1.254", "gateway": "172.16.1.1" },
    ],
    'Hosts' : [
        #{ 'name' : "os-controller" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" , "os-controller"), ], 'script' : "test.sh" },
        #{ 'name' : "os-network"    , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" , "os-network"),   ("os-dataplane"), ("os-provider","*") ] },
        { 'name' : "os-controller"    , 'image' : "os-controller" , 'flavor':"m1.large" , 'net' : [ ("routed-net" , "os-controller"),   ("os-dataplane"), ("os-provider","*") ] },
        { 'name' : "os-compute-1"  , 'image' : "os-compute-1" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"os-compute-1"),  ("os-dataplane"), ("os-provider","*") ] },
        { 'name' : "os-compute-2"  , 'image' : "os-compute-2" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" , "os-compute-2"), ("os-dataplane"), ("os-provider","*") ] },
        #{ 'name' : "os-controller"    , 'image' : "centos1602" , 'flavor':"m1.large" , 'net' : [ ("routed-net" , "os-controller"),   ("os-dataplane"), ("os-provider","*") ] },
        #{ 'name' : "os-compute-1"  , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"os-compute-1"),  ("os-dataplane"), ("os-provider","*") ] },
        #{ 'name' : "os-compute-2"  , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" , "os-compute-2"), ("os-dataplane"), ("os-provider","*") ] },
    ]
}
