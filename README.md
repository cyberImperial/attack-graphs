![ ](https://travis-ci.org/cyberImperial/attack-graphs.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/cyberImperial/attack-graphs/badge.svg?branch=master)](https://coveralls.io/github/cyberImperial/attack-graphs?branch=master)

# Attack-graphs

Run tests:
```
make test
coverage run setup.py test
```

To install the dependecies:
```
apt-get install libboost-all-dev -y
apt-get install libpcap-dev -y
python3 service.py install
make
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

NPM package:
```
npm install
npm start
```
