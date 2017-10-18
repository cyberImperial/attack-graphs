# Building the topology
```
We use traceroute from a host on a single subnet to get the path
to all other hosts on the subnet
sudo nmap -oX traceroute.xml -sn --traceroute 172.18.0.0/30
```
