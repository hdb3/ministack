
spec = {
    'name' : "sandbox VM",
    'external network name' : "exnet3",
    'keypair' : "X220",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "sandbox" , "start": "192.168.1.10", "end": "192.168.1.254", "subnet" :" 192.168.1.0/24", "gateway": "192.168.1.1" }
    ],
    'Hosts' : [
        { 'name' : "sandbox" , 'image' : "trusty64" , 'flavor':"m1.xlarge" , 'net' : [ ("sandbox" , "*", "sandbox" ) ] }
    ]
}
