import pd_base_tests
import pdb
import time
import sys

from collections import OrderedDict
from ptf import config
from ptf.testutils import *
from ptf.thriftutils import *

import os

from pal_rpc.ttypes import *

from aifo.p4_pd_rpc.ttypes import *
from mirror_pd_rpc.ttypes import *
from res_pd_rpc.ttypes import *

from tm_api_rpc.ttypes import *

from pkt_pd_rpc.ttypes import *


TCP_PORT = 8080
UDP_PORT = 9000
AIFO_PORT = 8888
UDP_DSTPORT = 8888

dev_id = 0
if (test_param_get("arch") == "tofino") or (test_param_get("arch") == "Tofino"):
  print("TYPE Tofino")
  sys.stdout.flush()
  MIR_SESS_COUNT = 1024
  MAX_SID_NORM = 1015
  MAX_SID_COAL = 1023
  BASE_SID_NORM = 1
  BASE_SID_COAL = 1016
elif (test_param_get("arch") == "tofino2") or (test_param_get("arch") == "Tofino2"):
  print("TYPE Tofino2")
  sys.stdout.flush()
  MIR_SESS_COUNT = 256
  MAX_SID_NORM = 255
  MAX_SID_COAL = 255
  BASE_SID_NORM = 0
  BASE_SID_COAL = 0
else:
  print("TYPE NONE")
  print(test_param_get("arch"))
  sys.stdout.flush()

ports = [188]

mirror_ids = []

dev_tgt = DevTarget_t(0, hex_to_i16(0xFFFF))

def setup_random(seed_val=0):
    if 0 == seed_val:
        seed_val = int(time.time())
    print("Seed is:", seed_val)
    sys.stdout.flush()
    random.seed(seed_val)

def make_port(pipe, local_port):
    assert(pipe >= 0 and pipe < 4)
    assert(local_port >= 0 and local_port < 72)
    return (pipe << 7) | local_port

def port_to_pipe(port):
    local_port = port & 0x7F
    assert(local_port < 72)
    pipe = (port >> 7) & 0x3
    assert(port == ((pipe << 7) | local_port))
    return pipe

def port_to_pipe_local_port(port):
    return port & 0x7F

swports = []
swports_by_pipe = {}
for device, port, ifname in config["interfaces"]:
    if port == 0: continue
    if port == 64: continue
    pipe = port_to_pipe(port)
    print(device, port, pipe, ifname)
    print(int(test_param_get('num_pipes')))
    if pipe not in swports_by_pipe:
        swports_by_pipe[pipe] = []
    if pipe in range(int(test_param_get('num_pipes'))):
        swports.append(port)
        swports.sort()
        swports_by_pipe[pipe].append(port)
        swports_by_pipe[pipe].sort()

if swports == []:
    for pipe in range(int(test_param_get('num_pipes'))):
        for port in range(1):
            swports.append( make_port(pipe,port) )
cpu_port = 64
#cpu_port = 192
print("Using ports:", swports)
sys.stdout.flush()

def mirror_session(mir_type, mir_dir, sid, egr_port=0, egr_port_v=False,
                   egr_port_queue=0, packet_color=0, mcast_grp_a=0,
                   mcast_grp_a_v=False, mcast_grp_b=0, mcast_grp_b_v=False,
                   max_pkt_len=9216, level1_mcast_hash=0, level2_mcast_hash=0,
                   mcast_l1_xid=0, mcast_l2_xid=0, mcast_rid=0, cos=0, c2c=0, extract_len=0, timeout=0,
                   int_hdr=[], hdr_len=0):
    return MirrorSessionInfo_t(mir_type,
                             mir_dir,
                             sid,
                             egr_port,
                             egr_port_v,
                             egr_port_queue,
                             packet_color,
                             mcast_grp_a,
                             mcast_grp_a_v,
                             mcast_grp_b,
                             mcast_grp_b_v,
                             max_pkt_len,
                             level1_mcast_hash,
                             level2_mcast_hash,
                             mcast_l1_xid,
                             mcast_l2_xid,
                             mcast_rid,
                             cos,
                             c2c,
                             extract_len,
                             timeout,
                             int_hdr,
                             hdr_len)

class AIFO_HDR(Packet):
    name = "AIFO_HDR"
    fields_desc = [
        XByteField("recirc_flag", 0),
        XIntField("flow_id", 0),
        XIntField("label", 0)
    ]

def aifo_packet(pktlen=0,
            eth_dst='00:11:11:11:11:11',
            eth_src='00:22:22:22:22:22',
            ip_src='0.0.0.2',
            ip_dst='0.0.0.1',
            udp_sport=8000,
            udp_dport=AIFO_PORT,
            recirc_flag=0,
            flow_id=0,
            label=0):
    udp_pkt = simple_udp_packet(pktlen=0,
                                eth_dst=eth_dst,
                                eth_src=eth_src,
                                ip_dst=ip_dst,
                                ip_src=ip_src,
                                udp_sport=udp_sport,
                                udp_dport=udp_dport)

    return udp_pkt / AIFO_HDR(recirc_flag=recirc_flag, flow_id=flow_id, label=label)

def scapy_aifo_bindings():
    bind_layers(UDP, AIFO_HDR, dport=AIFO_PORT)

def receive_packet(test, port_id, template):
    dev, port = port_to_tuple(port_id)
    (rcv_device, rcv_port, rcv_pkt, pkt_time) = dp_poll(test, dev, port, timeout=2)
    nrcv = template.__class__(rcv_pkt)
    return nrcv

def print_packet(test, port_id, template):
    receive_packet(test, port_id, template).show2()

def addPorts(test):
    test.pal.pal_port_add_all(dev_id, pal_port_speed_t.BF_SPEED_40G, pal_fec_type_t.BF_FEC_TYP_NONE)
    test.pal.pal_port_enable_all(dev_id)
    ports_not_up = True
    print("Waiting for ports to come up...")
    sys.stdout.flush()
    num_tries = 12
    i = 0
    while ports_not_up:
        ports_not_up = False
        for p in swports:
            x = test.pal.pal_port_oper_status_get(dev_id, p)
            if x == pal_oper_status_t.BF_PORT_DOWN:
                ports_not_up = True
                print("  port", p, "is down")
                sys.stdout.flush()
                time.sleep(3)
                break
        i = i + 1
        if i >= num_tries:
            break
    assert ports_not_up == False
    print("All ports up.")
    sys.stdout.flush()
    return



def init_tables(test, sess_hdl, dev_tgt):
    test.entry_hdls_ipv4 = []
    test.entry_hdls_ipv4_2 = []
    test.entry_flowrate_shl_0_table = []
    test.entry_flowrate_shl_1_table = []
    test.entry_flowrate_shl_2_table = []
    test.entry_flowrate_shl_3_table = []
    test.entry_check_uncongest_state_table = []

    ipv4_table_address_list = [0x0a010001, 0x0a010002, 0x0a010003, 0x0a010004, 0x0a010005,
        0x0a010006, 0x0a010007, 0x0a010008, 0x0a010009, 0x0a01000a, 0x0a01000b, 0x0a01000c, 0x01010101]
    ipv4_table_port_list = [188, 184, 180, 176, 172, 168, 164, 160, 156, 152, 148, 144, 320]

    tcp_port_list = []
    tcp_port = TCP_PORT
    for i in range(70):
        tcp_port_list.append(tcp_port)
        tcp_port += 1
    udp_port_list = []
    udp_port = UDP_PORT
    for i in range(70):
        udp_port_list.append(udp_port)
        udp_port += 1



    # add entries for ipv4 routing
    test.client.ipv4_route_set_default_action__drop(sess_hdl, dev_tgt)
    for i in range(len(ipv4_table_address_list)):
        match_spec = aifo_ipv4_route_match_spec_t(ipv4_table_address_list[i])
        action_spec = aifo_set_egress_action_spec_t(ipv4_table_port_list[i])
        entry_hdl = test.client.ipv4_route_table_add_with_set_egress(
            sess_hdl, dev_tgt, match_spec, action_spec)
        test.entry_hdls_ipv4.append(entry_hdl)

    # [add entry] set_ig_queue_length_table 
    # [add entry] get_eg_queue_length_table
    # [add entry] get_ig_queue_length_table
    # [add entry] set_eg_queue_length_table
    # [default]   get_qid_table
    # [default]   recirculate_table
    # [default]   get_info_table

    port_list = ipv4_table_port_list
    qid_list = range(0,32)
    index = 0
    for port in port_list:
        for qid in qid_list:
            index += 1
            match_spec = aifo_set_ig_queue_length_table_match_spec_t(port, qid)
            action_spec = aifo_set_ig_queue_length_action_action_spec_t(index)
            test.client.set_ig_queue_length_table_table_add_with_set_ig_queue_length_action(sess_hdl, dev_tgt, match_spec, action_spec)

            match_spec = aifo_get_eg_queue_length_table_match_spec_t(port, qid)
            action_spec = aifo_get_eg_queue_length_action_action_spec_t(index)
            test.client.get_eg_queue_length_table_table_add_with_get_eg_queue_length_action(sess_hdl, dev_tgt, match_spec, action_spec)

            match_spec = aifo_get_ig_queue_length_table_match_spec_t(port, qid)
            action_spec = aifo_get_ig_queue_length_action_action_spec_t(index)
            test.client.get_ig_queue_length_table_table_add_with_get_ig_queue_length_action(sess_hdl, dev_tgt, match_spec, action_spec)

            match_spec = aifo_set_eg_queue_length_table_match_spec_t(port, qid)
            action_spec = aifo_set_eg_queue_length_action_action_spec_t(index)
            test.client.set_eg_queue_length_table_table_add_with_set_eg_queue_length_action(sess_hdl, dev_tgt, match_spec, action_spec)

    test.client.get_qid_table_set_default_action_get_qid_action(sess_hdl, dev_tgt)
    test.client.recirculate_table_set_default_action_recirculate_action(sess_hdl, dev_tgt)
    test.client.get_info_table_set_default_action_get_info_action(sess_hdl, dev_tgt)

    # dstPort = 10000
    rank = 0
    flows_per_server = 8
    for srcAddr in ipv4_table_address_list:
        dstPort = 10000
        for inc in range(flows_per_server):
            match_spec = aifo_get_info_tcp_table_match_spec_t(srcAddr, dstPort)
            action_spec = aifo_get_info_tcp_action_action_spec_t(rank)
            test.client.get_info_tcp_table_table_add_with_get_info_tcp_action(sess_hdl, dev_tgt, match_spec, action_spec)
            rank += 1
            dstPort += 1
    
    

def clean_tables(test, sess_hdl, dev_id):
    print("closing session")


class SimpleTest(pd_base_tests.ThriftInterfaceDataPlane):
    def __init__(self):
        pd_base_tests.ThriftInterfaceDataPlane.__init__(self, ["aifo"])
        scapy_aifo_bindings()

    def runTest(self):
        sess_hdl = self.conn_mgr.client_init()
        self.sids = []
        try:
            if (test_param_get('target') == 'hw'):
                addPorts(self)
            else:
                print("test_param_get(target):", test_param_get('target'))

            sids = random.sample(xrange(BASE_SID_NORM, MAX_SID_NORM), len(swports))
            
            self.conn_mgr.complete_operations(sess_hdl)
            for sid in self.sids:
                self.mirror.mirror_session_enable(sess_hdl, Direction_e.PD_DIR_INGRESS, dev_tgt, sid)
            self.conn_mgr.complete_operations(sess_hdl)
            init_tables(self, sess_hdl, dev_tgt)
            self.conn_mgr.complete_operations(sess_hdl)
            print("INIT Finished.")
            sys.stdout.flush()

            while (True):
                time.sleep(1)
            self.conn_mgr.complete_operations(sess_hdl)
        finally:
            for sid in self.sids:
                self.mirror.mirror_session_disable(sess_hdl, Direction_e.PD_DIR_INGRESS, dev_tgt, sid)
            for sid in self.sids:
                self.mirror.mirror_session_delete(sess_hdl, dev_tgt, sid)
            clean_tables(self, sess_hdl, dev_id)