FROM ubuntu:16.04

RUN apt-get update
#RUN apt-get install metasploit-framework -y
RUN apt-get -y install vim curl make cmake wget
RUN apt-get -y install tar
RUN apt-get install nmap -y
RUN apt-get install tcpdump -y
RUN apt-get install git -y
RUN apt-get install net-tools -y
RUN apt-get install apache2 -y
RUN echo '<!doctype html><html><body><h1>This is a test web server.</h1></body></html>' | tee /var/www/html/index.html

EXPOSE 80


#Example exploit
#service postgreqsl start
#(!!!) if this is the first time you are running metasploit, run the following:
#msfdb init
#db_rebuild_cache
# start metasploit
#msfconsole

#Identify a remote host

#You can run nmap inside msfconsole and save its output into the MetaSploit database.
#db_nmap -v -sV host_or_network_to_scan[eg 192.168.0.0/24]
#This is a handy way to get an initial list of hosts on your network. I have some other tips in this linux commands for networking article
#To show a list of all available port scanners:
#search port-scan

#To list all the hosts found by nmap:

#hosts

#To add these hosts to your list of remote targets

#hosts -R



ENTRYPOINT service apache2 restart && /bin/bash
