
spec = {
    'name' : "ODL demo",
    'external network name' : "exnet3",
    'keypair' : "X220",
    'controller' : "r720",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    # 'credentials' : { 'user' : "admin", 'password' : "admin", 'project' : "admin" },
    # NOTE: network start/end range -
    #       a) must not include the gateway IP
    #       b) when assigning host IPs remember taht a DHCP server will be allocated from the range as well as the hosts
    #          Probably on the first or second available IP in the range....
    'Networks' : [
        { 'name' : "odldemo" , "start": "192.168.50.2", "end": "192.168.50.254", "subnet" :" 192.168.50.0/24", "gateway": "192.168.50.1" },
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "devstack-control" , 'image' : "trusty64" , 'flavor':"m1.xlarge" , 'net' : [ ("odldemo" , "192.168.50.20", "10.30.65.80") ] },
        { 'name' : "devstack-compute-1" , 'image' : "trusty64" , 'flavor':"m1.xlarge" , 'net' : [ ("odldemo" , "192.168.50.21","*") ] },
        # { 'name' : "devstack-compute-2" , 'image' : "trusty64" , 'flavor':"m1.xlarge" , 'net' : [ ("odldemo" , "192.168.50.22", None) ] },
        # { 'name' : "devstack-compute-3" , 'image' : "trusty64" , 'flavor':"m1.xlarge" , 'net' : [ ("odldemo" , "192.168.50.23", None) ] },
    ]
}
