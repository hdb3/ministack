
spec = {
    'name' : "compute server for mu mu",
    # 'routed network name' : "routed-net",
    'keypair' : "openstack_rsa",
    'controller' : "10.30.65.210",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "mumu", 'password' : "mumu", 'project' : "mumu" },
    'Networks' : [
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "mumu1" , 'image' : "ubuntu-15.10" , 'flavor':"m1.vast" , 'net' : [ ("routed-net" , "mumu1") ] },
    ]
}
