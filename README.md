#MiniStack

MiniStack is an orchestration tool for OpenStack. It brings the simplicty of Mininet topology creation in OpenStack, allowing for topologies to be rapidly built and reconfigured using a simple and extensible configuration format.

##Requirements

Python & pip

    ``apt-get install python-dev python-pip``
    
Python packages

    ``pip install -r requires.txt``

###Usage

    ./build.py -b spec.py

##Options

--auth -a
--dryrun -n
--build -b
--delete -d
--suspend -s
--resume -r
--complete -c

##Specification file
Used to specify resources, networks of the virtual machines you want to instantiate within an OpenStack infrastructure under a specific user.

###spec.py:


    spec = {

        'name' : "test project",

        'keypair' : "openstack_rsa",

        'controller' : "10.30.65.210",
        
        'dns' : "10.30.65.200",
        
        'credentials' : { 'user' : "Test", 'password' : "Test", 'project' : "Test" },
        
        'Networks' : [],
        
        'Hosts' : [ { 'name' : "test1" , 'image' : "ubuntu-15.10" , 'flavor':"m1.vast" , 'net' : [ ("routed-net" , "testnet1") ] },
        
        ]

    }


##Additional
Struggling to install OpenStack correctly?
Take a look at https://github.com/hdb3/openstack-build.git, an automated OpenStack installation script.

##TODO
Add more information on usage, options, and how to create your own spec file.
