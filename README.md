![ ](https://travis-ci.org/cyberImperial/attack-graphs.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/cyberImperial/attack-graphs/badge.svg?branch=master)](https://coveralls.io/github/cyberImperial/attack-graphs?branch=master)

# Attack-graphs

### Install
To install the dependecies:
```
apt-get install libboost-all-dev -y
apt-get install libpcap-dev -y
sudo python3 setup.py install
make
npm install
cd database && python3 load.py -r
```

Run tests:
```
make test
sudo python3 setup.py test
```

The inference engine depends on `mulval`. Please follow the instructions for installation from [here](http://people.cs.ksu.edu/~xou/mulval/). To run the inference engine, you need to set the following path variables: (in case they are not set, the module will try some default paths)
```
MULVALROOT=<mulval_path>
XSB_DIR=<xsb_path>
```

### Running the main application

The package needs elevated privileges as it runs the NIC in promiscuous mode.


Running a master node:
```
sudo python3 service.py master
```

Running a slave node:
```
sudo python3 service.py slave [master-ip]
``` 

Package options:
```
usage: service.py [-h] [-m MASTER] [-p PORT] [-i INTERFACE] [-s SIMULATION]
                  [-f FILTER] [-v]
                  type

positional arguments:
  type                  The type of node run: 'master' or 'slave'

optional arguments:
  -h, --help            show this help message and exit
  -m MASTER, --master MASTER
                        Specify master IP for connecting a slave.
  -p PORT, --port PORT  Specify port for runnning a slave.
  -i INTERFACE, --interface INTERFACE
                        The network interface listened to.
  -s SIMULATION, --simulation SIMULATION
                        To run a simulated network from a network
                        configuration file use this flag.
  -f FILTER, --filter FILTER
                        Specify a mask for filtering the packets. (e.g.
                        '10.1.1.1/16' would keep packets starting with '10.1')
  -v, --verbose         Set the logging level to DEBUG.
```

Running on a simulated network:
```
sudo python3 service.py master -s [simulation-config]
```

The configuration files for the simulated network should be placed inside the folder `simulation/confs`. The simulation module looks only for the files inside `simulation/confs`. For an example configuration see [simulation/confs/simple.json](https://github.com/cyberImperial/attack-graphs/blob/master/simulation/confs/simple.json):
```
sudo python3 service.py master -s simple.json
```

### Python CLI

Once the main application is running you can try to use individual component using interactive Python cli:
```
python3 service/cli.py
```

CLI options:
```
  -h, --help            show this help message and exit
  --echo ECHO [ECHO ...]
                        Usual echo command.
  --exit                Exit.
  --quit                Exit.
  --gen                 Send a request to the inference engine.
  --vul VUL VUL         Send a request to the database service for a
                        vulnerability. The first argument is the product. The
                        second argument is the version.
  --priv PRIV PRIV      Send a request to the database service for privilege
                        level escalation for a vulnerability. The first
                        argument is the product. The second argument is the
                        version. (e.g. `priv windows_2000 *`)
  --graph               Send a request to the local graph service.
  --packet              Send a request to the local sniffer service.
```

### Front-end

Staring the graphical user interface:
```
npm start
```
