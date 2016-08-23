
spec = {
    'name' : "a liberty cluster for testing cloudify",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    # 'credentials' : { 'user' : "cloudify", 'password' : "cloudify", 'project' : "cloudify" },
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        # { 'name' : "liberty" , "start": "192.168.0.2", "end": "192.168.0.254", "subnet" :" 192.168.0.0/24", "gateway": "192.168.0.1" },
        { 'name' : "cloudify-dataplane" , "subnet" :" 172.16.0.0/24" },
        { 'name' : "cloudify-provider" , "subnet" :" 172.16.1.0/24","start": "172.16.1.3", "end": "172.16.1.127", "gateway": "172.16.1.1" },
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "cloudify-controller" , 'image' : "centos1602" , 'flavor':"m1.large" , 'net' : [ ("routed-net" , "cloudify-controller"), ] },
        { 'name' : "cloudify-network" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"cloudify-network"), ("cloudify-dataplane"), ("cloudify-provider","*") ] },
        { 'name' : "cloudify-compute1" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"cloudify-compute1"), ("cloudify-dataplane"), ("cloudify-provider","*") ] },
        { 'name' : "cloudify-compute2" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"cloudify-compute2"), ("cloudify-dataplane"), ("cloudify-provider","*") ] },
        { 'name' : "cloudify-compute3" , 'image' : "centos1602" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" ,"cloudify-compute3"), ("cloudify-dataplane"), ("cloudify-provider","*") ] },
        { 'name' : "cloudify-cloudify" , 'image' : "centos1602" , 'flavor':"m1.medium" , 'net' : [ ("routed-net" , "cloudify-cloudify"), ("cloudify-provider","*") ] },
    ]
}
