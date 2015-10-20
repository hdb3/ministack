
spec = {
    'name' : "ODL demo",
    'external network name' : "exnet3",
    'keypair' : "X220",
    'controller' : "r720",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    # 'credentials' : { 'user' : "admin", 'password' : "admin", 'project' : "admin" },
    # NOTE: network start/end range -
    #       a) must not include the gateway IP
    #       b) when assigning host IPs remember taht a DHCP server will be allocated from the range as well as the hosts
    #          Probably on the first or second available IP in the range....
    'Networks' : [
        { 'name' : "kilo" , "start": "192.168.0.2", "end": "192.168.0.254", "subnet" :" 192.168.0.0/24", "gateway": "192.168.0.1" },
        { 'name' : "kilo-dataplane" , "start": "172.16.0.2", "end": "172.16.0.254", "subnet" :" 172.16.0.0/24", "gateway": "172.16.0.1" },
        { 'name' : "kilo-provider" , "start": "172.16.1.2", "end": "172.16.1.254", "subnet" :" 172.16.1.0/24", "gateway": "172.16.1.1" },
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "kilo-control" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [
                                                                                          ("kilo" , "192.168.0.20", "kilo-controller"),
                                                                                         ] },
        { 'name' : "kilo-compute-1" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [
                                                                                            ("kilo" , "192.168.0.21","kilo-compute"),
                                                                                            ("kilo-dataplane" , "" ),
                                                                                            ("kilo-provider" , "") ] },
        { 'name' : "kilo-network-1" , 'image' : "Centos7" , 'flavor':"m1.xlarge" , 'net' : [ ("kilo" , "192.168.0.22","kilo-network"), ("kilo-dataplane" , ""), ("kilo-provider" , "") ] },
    ]
}
