import socket
import struct
import time
import thread
import sys
import os
import select

MY_PORT = 50000 + 42

BUFSIZE = 1400

def receiver():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = MY_PORT
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rs.bind(('', port))
    t1 = time.time()
    count = 0
    while (1):
        packet_received, addr = rs.recvfrom(BUFSIZE)
        count += sys.getsizeof(packet_received)
        t2 = time.time()
        if t2 - t1 >= 5:
            print("[%d] Gbps:%0.2f"%(port, count*8/1e9/(t2-t1)))
            t1 = t2
            count = 0
            sys.stdout.flush()
        continue
def receiver_select():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
        port_2 = eval(sys.argv[3])
    else:
        port = MY_PORT
        port_2 = MY_SECOND_PORT
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rs.bind(('', port))
    rs_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rs_2.bind(('', port_2))
    inputs = [rs, rs_2]
    outputs = []
    t1 = time.time()
    count = 0
    while (1):
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            packet_received, addr = s.recvfrom(BUFSIZE)
            count += sys.getsizeof(packet_received)
            t2 = time.time()
            if t2 - t1 >= 5:
                print("bps:"+str(count*8/1e9/(t2-t1))+" once:"+str(sys.getsizeof(packet_received)))
                t1 = t2
                count = 0
        continue

def sender():
    if len(sys.argv) < 4:
        usage()
    count = int(eval(sys.argv[2]))
    host = sys.argv[3]
    if len(sys.argv) > 4:
        port = eval(sys.argv[4])
    else:
        port = MY_PORT
    testdata = 'x' * (BUFSIZE-1) + '\n'
    # testdata = 'x' * (100-1) + '\n'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i=0
    cc= 0 
    while i<count:
        i += 1
        s.sendto(testdata, (host, 9049 + cc))
        cc = cc + 1
        cc = cc % 8
        # time.sleep(100/1000000000.0)

def usage():
    sys.stdout = sys.stderr
    print 'Usage:    (on host_A) throughput -s [port]'
    print 'and then: (on host_B) throughput -c count host_A [port]'
    sys.exit(2)

def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        receiver()
    elif sys.argv[1] == '-c':
        sender()
    else:
        usage()
    
        
if __name__ == "__main__":
    main()