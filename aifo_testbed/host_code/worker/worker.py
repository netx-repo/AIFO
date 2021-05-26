#!/usr/bin/python

# A simple script to generate worker packets to carry queue length info
# between egress and ingress

import os
import sys
import socket
import struct

# from config import *

if len(sys.argv) <= 1:
    print("Usage")
    print("  python nc_socket.py 10.1.0.5 0 1 2 3")
    sys.exit()

headip = "10.1.0.4"

clientReadPort = 9999
clientWritePort = 7777

UCAST_EGRESS_PORT = 188
QID = 1
QUEUE_LENGTH = 2

try:
    ipAddr = sys.argv[1]
except:
    ipAddr = headip

try:
    ucast_egress_port = int(sys.argv[2])
except:
    ucast_egress_port = ACQUIRE_LOCK

try:
    qid = int(sys.argv[3])
except:
    qid = QID

try:
    queue_length = int(sys.argv[4])
except:
    queue_length = QUEUE_LENGTH

pkt = ""
pkt += struct.pack(">I", ucast_egress_port)
pkt += struct.pack(">I", qid)
pkt += struct.pack(">I", queue_length)


if 1 == 1:
    port = clientReadPort
else:
    port = clientWritePort

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(pkt, (ipAddr, port))