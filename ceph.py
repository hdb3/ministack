
spec = {
    'name' : "a 5-node ceph cluster",
    # 'routed network name' : "routed-net",
    'keypair' : "openstack_rsa",
    'controller' : "10.30.65.210",
    'dns' : "10.30.65.200",
    'credentials' : { 'user' : "nic", 'password' : "nic", 'project' : "nic" },
    'Networks' : [
        { 'name' : "ceph" , "start": "192.168.0.2", "end": "192.168.0.254", "subnet" :" 192.168.0.0/24", "gateway": "192.168.0.1" },
    ],
    # Hint: list explicity required external IPs first to avoid them being claimed by hosts that don't care...
    'Hosts' : [
        { 'name' : "vceph1" , 'image' : "centos7.2" , 'flavor':"m.ceph" , 'net' : [ ("routed-net" , "vceph1"), ("ceph","*") ], 'script' : "test.sh" },
        { 'name' : "vceph2" , 'image' : "centos7.2" , 'flavor':"m.ceph" , 'net' : [ ("routed-net" , "vceph2"), ("ceph","*") ], 'script' : "test.sh" },
        { 'name' : "vceph3" , 'image' : "centos7.2" , 'flavor':"m.ceph" , 'net' : [ ("routed-net" , "vceph3"), ("ceph","*") ], 'script' : "test.sh" },
        { 'name' : "vceph-openstack" , 'image' : "centos7.2" , 'flavor':"m1.xlarge" , 'net' : [ ("routed-net" , "vceph-openstack"), ("ceph","*") ], 'script' : "test.sh" },
        { 'name' : "vceph-client" , 'image' : "centos7.2" , 'flavor':"m1.medium" , 'net' : [ ("routed-net" , "vceph-client"), ("ceph","*") ], 'script' : "test.sh" },
    ]
}
