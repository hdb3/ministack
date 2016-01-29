
spec = {
    'name' : "a 4-node kilo cluster",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "kilo" , "start": "192.168.0.2", "end": "192.168.0.254", "subnet" :" 192.168.0.0/24", "gateway": "192.168.0.1" },
        { 'name' : "kilo-dataplane" , "subnet" :" 172.16.0.0/24" },
        { 'name' : "kilo-provider" , "subnet" :" 172.16.1.0/24","start": "172.16.1.3", "end": "172.16.1.254", "gateway": "172.16.1.1" },
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "kilo-controller" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [ ("kilo" , "192.168.0.20", "kilo-controller"),("kilo-dataplane"), ("kilo-provider","*") ], 'script' : "test.sh" },
        { 'name' : "kilo-compute-1" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [ ("kilo" , "192.168.0.101","kilo-compute-1"), ("kilo-dataplane"), ("kilo-provider","*") ] },
        { 'name' : "kilo-compute-2" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [ ("kilo" , "192.168.0.102","kilo-compute-2"), ("kilo-dataplane"), ("kilo-provider","*") ] },
    ]
}
