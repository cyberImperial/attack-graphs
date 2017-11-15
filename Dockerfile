FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install make cmake -y
RUN apt-get install libboost-all-dev -y
RUN apt-get install python3-pip -y
RUN apt-get install libpcap-dev -y
RUN pip3 install --upgrade requests
ADD . .
RUN make .

