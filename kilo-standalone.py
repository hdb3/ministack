
spec = {
    'name' : "a stand alone kilo instance",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "kilo-standalone" , "start": "192.168.0.2", "end": "192.168.0.254", "subnet" :" 192.168.0.0/24", "gateway": "192.168.0.1" },
        { 'name' : "kilo-standalone-dummy" , "subnet" :" 172.16.9.0/24" },
        { 'name' : "kilo-standalone-provider" , "subnet" :" 172.16.1.0/24" },
    ],
    'Hosts' : [
        { 'name' : "kilo-standalone" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [ ("kilo-standalone" , "192.168.0.101","kilo-standalone"), ("kilo-standalone-dummy"), ("kilo-standalone-provider") ] },
    ]
}
