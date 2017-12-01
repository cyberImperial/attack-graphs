![ ](https://travis-ci.org/cyberImperial/attack-graphs.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/cyberImperial/attack-graphs/badge.svg?branch=master)](https://coveralls.io/github/cyberImperial/attack-graphs?branch=master)

# Attack-graphs

To install the dependecies:
```
apt-get install libboost-all-dev -y
apt-get install libpcap-dev -y
python3 service.py install
make
npm install
cd database && python3 load.py -r
```

Run tests:
```
make test
coverage run setup.py test
```

Help:
```
sudo python3 service.py -h
```

Running a master node:
```
sudo python3 service.py master
```

Running a slave node:
```
sudo python3 service.py slave [master-ip]
```

The package needs elevated privileges as it runs the NIC in promiscuous mode.

Staring the interface:
```
npm start
```
