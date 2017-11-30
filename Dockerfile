FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install make cmake vim iputils-ping -y
RUN apt-get install libboost-all-dev -y
RUN apt-get install python3-pip -y
RUN apt-get install libpcap-dev -y
RUN pip3 install --upgrade requests

RUN apt-get -y install vim curl make cmake wget
RUN apt-get -y install tar
RUN apt-get install nmap -y
RUN apt-get install tcpdump -y
RUN apt-get install git -y
RUN apt-get install net-tools -y

RUN pip3 install Flask

RUN pip3 install pcapy
RUN git clone https://github.com/cyberImperial/attack-graphs.git
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
# RUN cd attack-graphs && cd database && python3 load.py -r
RUN cd attack-graphs && make .
