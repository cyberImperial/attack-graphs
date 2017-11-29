import socket
from struct import *
import datetime
import pcapy
import sys

def main(argv):
    #list all devices
    devices = pcapy.findalldevs()
    print(devices)

    #ask user to enter device name to sniff
    print("Available devices are :")
    for d in devices :
        print(d)

    dev = "".join(list(input("Enter device name to sniff : ")))
    print("Sniffing device: " + dev)

    '''
    open device
    # Arguments here are:
    #   device
    #   snaplen (maximum number of bytes to capture _per_packet_)
    #   promiscious mode (1 for true)
    #   timeout (in milliseconds)
    '''
    cap = pcapy.open_live(dev , 65536 , 1 , 0)

    #start sniffing packets
    while(1) :
        (header, packet) = cap.next()
        packet = parse_packet(packet)
        if packet is not None:
            print(packet)

#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b


#Protocol numbers in IP header(ICMP:1, TCP:6, UDP:17)
#https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
IP_PROTOCOL_NUMBER = 8
ICMP_NUMBER = 1
TCP_NUMBER = 6
UDP_NUMBER = 17

#function to parse a packet
def parse_packet(packet) :
   packet_json = {}

   #parse ethernet header
   eth_length = 14

   eth_header = packet[:eth_length]
   eth = unpack('!6s6sH', eth_header)
   eth_protocol = socket.ntohs(eth[2])
  # print "Destination MAC: " + eth_addr(packet[0:6]) + " Source MAC: " + eth_addr(packet[6:12]) + " Protocol: " + str(eth_protocol)

   #Parse IP header, IP protocol number:8
   if eth_protocol == IP_PROTOCOL_NUMBER:
       #Parse IP header
       #take first 20 characters for the ip header
       ip_header = packet[eth_length:20+eth_length]

       #now unpack them
       iph = unpack('!BBHHHBBH4s4s',ip_header)

       version_ihl = iph[0]
       version = version_ihl >> 4
       ihl = version_ihl & 0xF

       iph_length = ihl * 4

       ttl = iph[5]
       protocol = iph[6]
       s_addr = socket.inet_ntoa(iph[8])
       d_addr = socket.inet_ntoa(iph[9])

       packet_json = {
         "version" : str(version),
         "ip_header_length" : str(ihl),
         "ttl" : str(ttl),
         "src" : str(s_addr),
         "dest" : str(d_addr)
       }

     # print(packet_json)

       # TCP protocol
       if protocol ==  TCP_NUMBER:
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]

            #now unpack them :)
            tcph = unpack('!HHLLBBHHH' , tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4

            packet_json["transport_type"] = "TCP"
            packet_json["transport"] = {
              "src_port" : str(source_port),
              "dest_port" : str(dest_port),
              "seq" : str(sequence),
              "ack" : str(acknowledgement),
            }

            #h_size = eth_length + iph_length + tcph_length * 4
            #data_size = len(packet) - h_size

            #get data from the packet
            #data = packet[h_size:]
            #print 'Data : ' + data

       #ICMP Packets
       elif protocol == ICMP_NUMBER:
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u+4]

            #now unpack them :)
            icmph = unpack('!BBH' , icmp_header)

            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]

            packet_json["transport_type"] = "ICMP"
            packet_json["transport"] = {
              "type" : str(icmp_type),
              "code" : str(code),
              "checksum" : str(checksum)
            }

            # h_size = eth_length + iph_length + icmph_length
            # data_size = len(packet) - h_size
            #
            # #get data from the packet
            # data = packet[h_size:]
            #
            # print 'Data : ' + data

       #UDP packets
       elif protocol == UDP_NUMBER:
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u+8]

            #now unpack them :)
            udph = unpack('!HHHH' , udp_header)

            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]

            packet_json["transport_type"] = "UDP"
            packet_json["transport"] = {
              "src_port" : str(source_port),
              "dest_port" : str(dest_port),
              "length" : str(length),
              "checksum" : str(checksum)
            }
            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size

            #get data from the packet
            # data = packet[h_size:]

            # print 'Data : ' + data

       #some other IP packet like IGMP
       else:
            packet_json ["transport_type"] = "other"
       return packet_json
   return None

if __name__ == "__main__":
  main(sys.argv)
