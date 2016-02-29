
spec = {
    'name' : "The devil's work...",
    'external network name' : "exnet3",
    'keypair' : "openstack_rsa",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "merlynctl" , "start": "172.16.1.2", "end": "172.16.1.100", "subnet" :" 172.16.1.0/24", "gateway": "172.16.1.1" },
        { 'name' : "merlyn201" , "start": "192.168.1.201", "end": "192.168.1.202", "subnet" :" 192.168.1.0/24", "vlan": 201, "physical_network": "vlannet" },
        { 'name' : "merlyn202" , "start": "192.168.1.202", "end": "192.168.1.203", "subnet" :" 192.168.1.0/24", "vlan": 202, "physical_network": "vlannet" }
    ],
    'Hosts' : [
        { 'name' : "monos" , 'image' : "centos7.2" , 'flavor':"m1.large" , 'net' : [ ("merlynctl","*","10.30.65.130")] },
        { 'name' : "m201" , 'image' : "centos7.2" , 'flavor':"m1.medium" , 'net' : [ ("merlynctl","*","10.30.65.131"),("merlyn201" , "192.168.1.201") ] },
        { 'name' : "m202" , 'image' : "centos7.2" , 'flavor':"m1.medium" , 'net' : [ ("merlynctl","*","10.30.65.132"),("merlyn202" , "192.168.1.202") ] },
    ]
}
