from __future__ import absolute_import
from unittest import TestCase

from topology.fw.sniffer import parse_packet

class TestParsePacket(TestCase):
    RAW_PACKET = b'\\\x93\xa2\xf4\xf7\xf6\xf0\x9f\xc2\x18\xa2\xdf\x08\x00E\x00\x004x\x98@\x00:\x06\x84Yh\x10\x19\xeb\xc0\xa8\x01/\x01\xbb\xb0\xf0v\xb1j.\xc2^L\xe3\x80\x10\x00 t\x99\x00\x00\x01\x01\x05\n\xc2^L\xc3\xc2^L\xe3'
    RES_PACKET = {
        'dest': '192.168.1.47',
        'src': '104.16.25.235',
        'version': '4',
        'ip_header_length': '5',
        'ttl': '58',
        'transport': {
            'src_port': '443',
            'ack': '3260959971',
            'dest_port': '45296',
            'seq': '1991338542'
        },
        'transport_type': 'TCP'
    }

    def deep_compare(self, json1, json2):
        if type(json1) == str:
            return json1 == json2
        if len(json1) == len(json2):
            return False
        return all([deep_compare(json1[entry], json2[entry])
            for entry in json1])

    def test_tcp_packet(self):
        packet = parse_packet(self.RAW_PACKET)
        self.deep_compare(packet, self.RES_PACKET)
