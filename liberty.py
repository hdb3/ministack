
spec = {
    'name' : "a 4-node liberty cluster",
    # 'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        # { 'name' : "liberty" , "start": "192.168.0.2", "end": "192.168.0.254", "subnet" :" 192.168.0.0/24", "gateway": "192.168.0.1" },
        { 'name' : "liberty-dataplane" , "subnet" :" 172.16.0.0/24" },
        { 'name' : "liberty-provider" , "subnet" :" 172.16.1.0/24","start": "172.16.1.3", "end": "172.16.1.254", "gateway": "172.16.1.1" },
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "liberty-controller" , 'image' : "centos1602" , 'flavor':"m1.large" , 'net' : [ ("routed-net" , "liberty-controller"), ] },
        { 'name' : "liberty-network" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"liberty-network"), ("liberty-dataplane"), ("liberty-provider","*") ] },
        { 'name' : "liberty-compute1" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"liberty-compute1"), ("liberty-dataplane"), ("liberty-provider","*") ] },
        { 'name' : "liberty-compute2" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"liberty-compute2"), ("liberty-dataplane"), ("liberty-provider","*") ] },
        { 'name' : "liberty-cloudify" , 'image' : "centos1602" , 'flavor':"m1.medium" , 'net' : [ ("routed-net" , "liberty-cloudify"), ("liberty-provider","*") ] },
    ]
}
