import sys, os, time, subprocess, random
import paramiko
import threading
from multiprocessing import Process
from config import *

WPKTS_SEND_LIMIT_MS = 3000
thread_per_client = 1
udp_thread_per_client = 1

tenant_group = [0, 1,1,1,1, 1,1,1,1, 1,1,1,1]

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

dstIP_list = ["null", "10.1.0.6", "10.1.0.6", "10.1.0.6", "10.1.0.6",
            "10.1.0.6", "10.1.0.6", "10.1.0.8", "10.1.0.8", "10.1.0.9", "10.1.0.9", "10.1.0.12", "10.1.0.12"]
dstPort_list = ["0", "8080", "8081", "8082", "8083", 
            "8084", "8085", "8080", "8080", "8080", "8080", "8080", "8080"]
srcPort_list = ["0", "8080", "8080", "8080", "8080", 
            "8080", "8080", "8080", "8080", "8080", "8080", "8080", "8080"]

def dstIP(client_id):
    return dstIP_list[int(client_id)]

def dstPort(client_id):
    return dstPort_list[int(client_id)]

def srcPort(server_id):
    return srcPort_list[int(server_id)]

class CSFQConsole(object):
    def to_hostname(self, client_name):
        return id_to_hostname_dict[client_name]

    def to_username(self, client_name):
        return id_to_username_dict[client_name] 

    def to_passwd(self, client_name):
        return id_to_passwd_dict[client_name]

    def __init__(self, client_names, server_names, worker_name, switch_name):
        #### TODO: modify because there is no TCP&UDP mixed traffic.
        self.wpkts_send_limit_ms_client = WPKTS_SEND_LIMIT_MS
        self.wpkts_send_limit_ms_server = WPKTS_SEND_LIMIT_MS

        self.program_name = "aifo"
        self.sppifo_name = "sppifo"
        self.simple_switch_name = "simpleswitch"
        self.ecn_switch_name = "ecnswitch"
        self.server_names = server_names
        self.client_names = client_names
        self.switch_name  = switch_name
        self.worker_name = worker_name
        
        self.passwd = {}
        for client_name in client_names:
            self.passwd[client_name] = id_to_passwd_dict[client_name]

        for client_name in server_names:
            self.passwd[client_name] = id_to_passwd_dict[client_name]

        for client_name in worker_name:
            self.passwd[client_name] = id_to_passwd_dict[client_name]


        self.switch_pw = id_to_passwd_dict[switch_name]

        self.worker = []
        for client_name in worker_name:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(hostname = self.to_hostname(client_name), username = self.to_username(client_name), password = self.passwd[client_name])
            self.worker.append((client_name, client))

        self.clients = []
        for client_name in client_names:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(hostname = self.to_hostname(client_name), username = self.to_username(client_name), password = self.passwd[client_name])
            self.clients.append((client_name, client))

        

        self.servers = []
        for server_name in server_names:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(hostname = self.to_hostname(server_name), username = self.to_username(server_name), password = self.passwd[server_name])
            self.servers.append((server_name, client))

        switch = paramiko.SSHClient()
        switch.load_system_host_keys()
        switch.connect(hostname = self.to_hostname(self.switch_name), username = self.to_username(switch_name), password = self.switch_pw)
        self.switch = (self.switch_name, switch)

        self.local_home_dir = local_home_dir
        self.local_main_dir = self.local_home_dir + "aifo_testbed/"
        self.local_p4_dir   = self.local_home_dir + "aifo_testbed/aifo_switch/p4src/"
        self.local_ptf_dir  = self.local_home_dir + "aifo_testbed/aifo_switch/controller/"
        self.local_res_dir  = self.local_home_dir + "aifo_testbed/results/"
        self.local_client_dir = self.local_home_dir + "aifo_testbed/host_code/incast_dpdk/client/"
        self.local_server_dir = self.local_home_dir + "aifo_testbed/host_code/incast_dpdk/server/"
        self.local_simple_switch_dir = self.local_home_dir + "aifo_testbed/simple_switch/"
        self.local_simple_switch_p4_dir = self.local_home_dir + "aifo_testbed/simple_switch/p4src/"
        self.local_simpletcp_dir = self.local_home_dir + "aifo_testbed/host_code/simple_tcp/"
        self.local_worker_dir = self.local_home_dir + "aifo_testbed/host_code/worker/"

        self.remote_server_home_dir = remote_server_home_dir
        self.remote_server_main_dir = self.remote_server_home_dir + "aifo_testbed/"
        self.remote_server_client_dir = self.remote_server_home_dir + "aifo_testbed/host_code/incast_dpdk/client/"
        self.remote_server_server_dir = self.remote_server_home_dir + "aifo_testbed/host_code/incast_dpdk/server/"
        self.remote_server_log_dir  = self.remote_server_home_dir + "aifo_testbed/logs/"
        self.remote_server_res_dir  = self.remote_server_home_dir + "aifo_testbed/results/"
        self.remote_server_ptf_dir = self.remote_server_home_dir + "aifo_testbed/aifo_switch/controller/"
        self.remote_server_dpdk_dir = self.remote_server_home_dir + "aifo_testbed/host_code/incast_dpdk/"
        self.remote_server_simpletcp_dir = self.remote_server_home_dir + "aifo_testbed/host_code/simple_tcp/"
        self.remote_server_worker_dir = self.remote_server_home_dir + "aifo_testbed/host_code/worker/"

        self.remote_switch_home_dir = remote_switch_home_dir
        self.remote_switch_main_dir = self.remote_switch_home_dir + "aifo_testbed/aifo_switch/"
        self.remote_switch_p4_dir   = self.remote_switch_home_dir + "aifo_testbed/aifo_switch/p4src/"
        self.remote_switch_ptf_dir  = self.remote_switch_home_dir + "aifo_testbed/aifo_switch/controller/"
        self.remote_switch_log_dir  = self.remote_switch_home_dir + "aifo_testbed/logs/"
        self.remote_switch_simple_switch_p4_dir = self.remote_switch_home_dir + "aifo_testbed/simple_switch/p4src/"
        self.remote_switch_simple_switch_ptf_dir = self.remote_switch_home_dir + "aifo_testbed/simple_switch/controller_init/"
        self.remote_switch_ecn_switch_p4_dir = self.remote_switch_home_dir + "aifo_testbed/ecn_switch/p4src/"
        self.remote_switch_ecn_switch_ptf_dir = self.remote_switch_home_dir + "aifo_testbed/ecn_switch/controller/"
        self.remote_switch_sppifo_p4_dir = self.remote_switch_home_dir + "aifo_testbed/sppifo/p4src/"
        self.remote_switch_sppifo_ptf_dir = self.remote_switch_home_dir + "aifo_testbed/sppifo/controller/"

        self.remote_switch_sde_dir  = remote_switch_sde_dir
             
        print("========init completed========")


    # ********************************
    # fundamental functions
    # ********************************

    def exe(self, client, cmd, with_print=False):
        (client_name, client_shell) = client
        stdin, stdout, stderr = client_shell.exec_command(cmd)
        if with_print:
            print(client_name, ":", stdout.read(), stderr.read())

    def sudo_exe(self, client, cmd, with_print=False):
        (client_name, client_shell) = client
        cmdheader = "echo '%s' | sudo -S " %(self.passwd[client_name])
        cmd = cmdheader + cmd
        stdin, stdout, stderr = client_shell.exec_command(cmd)
        if with_print:
            print(client_name, ":", stdout.read(), stderr.read())
            stdout.flush()
            stderr.flush()

    def kill_host(self):
        #### TODO: check if every line is needed, and all processes are covered
        for client in self.clients:
            self.sudo_exe(client, "pkill client")
            self.sudo_exe(client, "pkill server")
            self.sudo_exe(client, "pkill epwget")
            self.sudo_exe(client, "pkill epserver")
            self.sudo_exe(client, "pkill python")
            self.sudo_exe(client, "pkill iperf3")
            self.sudo_exe(client, "pkill tcpdump")
        # time.sleep(2)
        for server in self.servers:
            self.sudo_exe(server, "pkill client")
            self.sudo_exe(server, "pkill server")
            self.sudo_exe(server, "pkill epwget")
            self.sudo_exe(server, "pkill epserver")
            self.sudo_exe(server, "pkill python")
            self.sudo_exe(server, "pkill iperf3")
            self.sudo_exe(server, "pkill tcpdump")

    def kill_switch(self):
        self.exe(self.switch, "ps -ef | grep switchd | grep -v grep | " \
            "awk '{print $2}' | xargs kill -9")
        self.exe(self.switch, "ps -ef | grep run_p4_test | grep -v grep | " \
            "awk '{print $2}' | xargs kill -9")
        self.exe(self.switch, "ps -ef | grep tofino | grep -v grep | " \
            "awk '{print $2}' | xargs kill -9")

    def kill_all(self):
        self.kill_host()
        self.kill_switch()
    
    def init_sync_host(self):
        for client in self.client_names + self.server_names + self.worker_name:
            cmd = "scp -r %s %s@%s:%s" % (self.local_main_dir, self.to_username(client), self.to_hostname(client), self.remote_server_home_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)

    def init_sync_switch(self):
        cmd = "scp -r %s %s@%s:%s" % (self.local_main_dir, self.to_username(self.switch_name), self.to_hostname(self.switch_name), self.remote_switch_home_dir)
        print(cmd)
        subprocess.call(cmd, shell = True)

    def sync_host(self):
        for worker in self.worker_name:
            cmd = "rsync -r %s %s@%s:%s" % (self.local_worker_dir, self.to_username(worker), self.to_hostname(worker), self.remote_server_worker_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)

        for client in self.client_names:
            cmd = "rsync -r %s %s@%s:%s" % (self.local_client_dir, self.to_username(client), self.to_hostname(client), self.remote_server_client_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
            cmd = "rsync -r %s %s@%s:%s" % (self.local_ptf_dir, self.to_username(client), self.to_hostname(client), self.remote_server_ptf_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
            cmd = "rsync -r %s %s@%s:%s" % (self.local_simpletcp_dir, self.to_username(client), self.to_hostname(client), self.remote_server_simpletcp_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)


        for server in self.server_names:
            cmd = "rsync -r %s %s@%s:%s" % (self.local_server_dir, self.to_username(server), self.to_hostname(server), self.remote_server_server_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
            cmd = "rsync -r %s %s@%s:%s" % (self.local_ptf_dir, self.to_username(server), self.to_hostname(server), self.remote_server_ptf_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
            cmd = "rsync -r %s %s@%s:%s" % (self.local_simpletcp_dir, self.to_username(server), self.to_hostname(server), self.remote_server_simpletcp_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
        return

    def sync_switch(self):
        cmd = "scp -r %s %s@%s:%s" % (self.local_p4_dir, self.to_username(self.switch_name), self.to_hostname(self.switch_name), self.remote_switch_main_dir)
        print(cmd)
        subprocess.call(cmd, shell = True)
        cmd = "scp -r %s %s@%s:%s" % (self.local_ptf_dir, self.to_username(self.switch_name), self.to_hostname(self.switch_name), self.remote_switch_main_dir)
        print(cmd)
        subprocess.call(cmd, shell = True)
        return

    def sync_all(self):
        self.sync_switch()
        self.sync_host()
        return

    def compile_host(self):
        for client in self.clients:
            dpdk_dir = self.remote_server_client_dir
            cmd = "source ~/.bash_profile;cd %s; make > %s/dpdk_client_compile.log 2>&1 &" % (dpdk_dir, self.remote_server_log_dir)
            print("%s compile client_dpdk: %s" % (client[0], cmd))
            self.exe(client, cmd, True)
        
        for server in self.servers:
            dpdk_dir = self.remote_server_server_dir
            cmd = "source ~/.bash_profile;cd %s; make > %s/dpdk_server_compile.log 2>&1 &" % (dpdk_dir, self.remote_server_log_dir)
            print("%s compile server_dpdk: %s" % (server[0], cmd))
            self.exe(server, cmd, True)
        return

    def compile_aifo(self):
        sde_dir = self.remote_switch_sde_dir
        p4_build = sde_dir + "p4_build.sh"
        p4_program = self.remote_switch_p4_dir + self.program_name + ".p4"
        cmd = "cd %s;source ./set_sde.bash;%s %s > %s/aifo_compile.log 2>&1 &" % (sde_dir, p4_build,
            p4_program, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)
        return

    def compile_sppifo(self):
        sde_dir = self.remote_switch_sde_dir
        p4_build = sde_dir + "p4_build.sh"
        p4_program = self.remote_switch_sppifo_p4_dir + self.sppifo_name + ".p4"
        cmd = "cd %s;source ./set_sde.bash;%s %s > %s/sppifo_compile.log 2>&1 &" % (sde_dir, p4_build,
            p4_program, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)
        return

    def compile_sw(self):
        sde_dir = self.remote_switch_sde_dir
        p4_build = sde_dir + "p4_build.sh"
        p4_program = self.remote_switch_simple_switch_p4_dir + self.simple_switch_name + ".p4"
        cmd = "cd %s;source ./set_sde.bash;%s %s > %s/fifo_compile.log 2>&1 &" % (sde_dir, p4_build,
            p4_program, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)
        return

    def compile_all(self):
        self.compile_host()
        self.compile_aifo()
        return

    def run_client(self):
        dpdk_dir = self.remote_server_client_dir
        port_st = 9000
        time_to_run = 50
        client_id = 0
        for client in self.clients:
            # client_id = client[0].strip("netx")
            client_id += 1
            tenant_id = tenant_group[int(client_id)]
            server_id = self.servers[0][0].strip("netx")
            
            cmd = "cd %s;source ~/.bash_profile; echo '%s' | sudo -S %s/build/client --lcores 0@0,1@1,2@2,3@3,4@4,5@5,6@6,7@7 -- -n%s -t%s -r%s -s%s -p%d -T%d" %\
                 (self.remote_server_client_dir, self.passwd[client[0]], dpdk_dir, client_id, tenant_id, server_id, int(self.wpkts_send_limit_ms_client), port_st, time_to_run) + " > %s/client_run_even_%s.log 2>&1 &" % (self.remote_server_res_dir, client_id)
            
            print("%s run client_dpdk: %s" % (client[0], cmd))
            self.exe(client, cmd, True)
            # time_to_run = time_to_run - 16
            time.sleep(10)
        return

    def run_server(self):
        dpdk_dir = self.remote_server_server_dir
        for server in self.servers:
            server_id = server[0].strip("netx")
            cmd = "cd %s;source ~/.bash_profile; echo '%s' | sudo -S %s/build/server --lcores 0@0,1@1,2@2,3@3,4@4,5@5,6@6,7@7 > %s/server_run.log 2>&1 &" %\
                (self.remote_server_server_dir, self.passwd[server[0]], dpdk_dir, self.remote_server_res_dir)
            print("%s run server_dpdk: %s" % (server[0], cmd))
            self.exe(server, cmd, True)
        return

    def run_server(self, alg):
        dpdk_dir = self.remote_server_server_dir
        for server in self.servers:
            server_id = server[0].strip("netx")
            cmd = "cd %s;source ~/.bash_profile; echo '%s' | sudo -S %s/build/server --lcores 0@0,1@1,2@2,3@3,4@4,5@5,6@6,7@7 > %s/server_run_%s.log 2>&1 &" %\
                (self.remote_server_server_dir, self.passwd[server[0]], dpdk_dir, self.remote_server_res_dir, alg)
            print("%s run server_dpdk: %s" % (server[0], cmd))
            self.exe(server, cmd, True)
        return

    def setup_tc(self):
        #### TODO: check if we actually use that, remove it if we don't use it
        if len(sys.argv)<=3:
            print_usage()
            sys.exit(0)
        target_id = sys.argv[2]
        rtt = sys.argv[3]
        print(target_id, rtt)
        for client in self.clients:
            client_id = client[0].strip("netx")
            if (client_id == target_id):
                cmd = "tc qdisc del dev enp5s0f0 root"
                print("%s clear tc: %s" % (client[0], cmd))
                self.sudo_exe(client, cmd, True)
                cmd = "tc qdisc add dev enp5s0f0 root netem delay %sms" % (rtt)
                print("%s set tc: %s" % (client[0], cmd))
                self.sudo_exe(client, cmd, True)
                break
        return

    def clear_tc(self):
        #### TODO: check if we actually use that, remove it if we don't use it
        if len(sys.argv)<=2:
            print_usage()
            sys.exit(0)
        target_id = sys.argv[2]
        print(target_id)
        for client in self.clients:
            client_id = client[0].strip("netx")
            if (client_id == target_id):
                cmd = "tc qdisc del dev enp5s0f0 root"
                print("%s clear tc: %s" % (client[0], cmd))
                self.sudo_exe(client, cmd, True)
                break
        return

    def setup_arp_worker(self):
        for client in self.worker:
            client_id = client[0].strip("netx")
            cmd = "cd %s/arp_conf/; while true; do echo '%s' | sudo -S ./%sarp.sh; done > /dev/null 2>&1 &" % (self.remote_server_main_dir, self.to_passwd(client[0]), client_id)
            print("%s set arp" % (client[0]))
            self.exe(client, cmd, True)
        return

    def setup_arp_host(self):
        for client in self.clients:
            client_id = client[0].strip("netx")
            # cmd = "cd %s/arp_conf/; sh loop.sh > /dev/null 2>&1 &" % (self.local_main_dir)
            cmd = "cd %s/arp_conf/; while true; do echo '%s' | sudo -S ./%sarp.sh; done > /dev/null 2>&1 &" % (self.remote_server_main_dir, self.to_passwd(client[0]), client_id)
            print("%s set arp" % (client[0]))
            self.exe(client, cmd, True)
    
        for server in self.servers:
            server_id = server[0].strip("netx")
            # cmd = "cd %s/arp_conf/; sh loop.sh > /dev/null 2>&1 &" % (self.local_main_dir)
            cmd = "cd %s/arp_conf/; while true; do echo '%s' | sudo -S ./%sarp.sh; done > /dev/null 2>&1 &" % (self.remote_server_main_dir, self.to_passwd(server[0]), server_id)
            print("%s set arp" % (server[0]))
            self.exe(server, cmd, True)
        return

    def setup_arp(self):
        #### TODO: check sysctl net.ipv4.tcp_congestion_control=cubic
        for client in self.worker:
            client_id = client[0].strip("netx")
            cmd = "cd %s/arp_conf/; while true; do echo '%s' | sudo -S ./%sarp.sh; done > /dev/null 2>&1 &" % (self.remote_server_main_dir, self.to_passwd(client[0]), client_id)
            print("%s set arp" % (client[0]))
            self.exe(client, cmd, True)

        for client in self.clients:
            client_id = client[0].strip("netx")
            # cmd = "cd %s/arp_conf/; sh loop.sh > /dev/null 2>&1 &" % (self.local_main_dir)
            cmd = "cd %s/arp_conf/; while true; do echo '%s' | sudo -S ./%sarp.sh; done > /dev/null 2>&1 &" % (self.remote_server_main_dir, self.to_passwd(client[0]), client_id)
            
            print("%s set arp" % (client[0]))
            self.exe(client, cmd, True)
    
        for server in self.servers:
            server_id = server[0].strip("netx")
            # cmd = "cd %s/arp_conf/; sh loop.sh > /dev/null 2>&1 &" % (self.local_main_dir)
            cmd = "cd %s/arp_conf/; while true; do echo '%s' | sudo -S ./%sarp.sh; done > /dev/null 2>&1 &" % (self.remote_server_main_dir, self.to_passwd(server[0]), server_id)
            print("%s set arp" % (server[0]))
            self.exe(server, cmd, True)
        return

    def kill_arp_host(self):
        for client in self.clients:
            client_id = client[0].strip("netx")
            cmd = "ps -ef | grep %sarp | grep -v grep | awk '{print $2}' | xargs kill -9" % (client_id)
            # cmd = "ps -ef | grep arp | grep -v grep | awk '{print $2}' | xargs kill -9"
            print("%s kill arp" % (client[0]))
            self.sudo_exe(client, cmd, True)

        for server in self.servers:
            server_id = server[0].strip("netx")
            cmd = "ps -ef | grep %sarp | grep -v grep | awk '{print $2}' | xargs kill -9" % (server_id)
            # cmd = "ps -ef | grep arp | grep -v grep | awk '{print $2}' | xargs kill -9"
            print("%s kill arp" % (server[0]))
            self.sudo_exe(server, cmd, True)
        return

    def kill_arp(self):
        for client in self.worker:
            client_id = client[0].strip("netx")
            cmd = "ps -ef | grep %sarp | grep -v grep | awk '{print $2}' | xargs kill -9" % (client_id)
            # cmd = "ps -ef | grep arp | grep -v grep | awk '{print $2}' | xargs kill -9"
            print("%s kill arp" % (client[0]))
            self.sudo_exe(client, cmd, True)

        for client in self.clients:
            client_id = client[0].strip("netx")
            cmd = "ps -ef | grep %sarp | grep -v grep | awk '{print $2}' | xargs kill -9" % (client_id)
            # cmd = "ps -ef | grep arp | grep -v grep | awk '{print $2}' | xargs kill -9"
            print("%s kill arp" % (client[0]))
            self.sudo_exe(client, cmd, True)

        for server in self.servers:
            server_id = server[0].strip("netx")
            cmd = "ps -ef | grep %sarp | grep -v grep | awk '{print $2}' | xargs kill -9" % (server_id)
            # cmd = "ps -ef | grep arp | grep -v grep | awk '{print $2}' | xargs kill -9"
            print("%s kill arp" % (server[0]))
            self.sudo_exe(server, cmd, True)
        return

    def run_tcp_client(self):        
        port_st = 10000
        index = 0
        log_id = 0
        for client in self.clients:
            server = self.servers[index]
            server_id = server[0].strip("netx")
            client_id = client[0].strip("netx")
            log_id = log_id + 1
            log_file = self.remote_server_res_dir + "/%s.log" % (log_id)
            cmd = "cd %s; cd host_code/simple_tcp; python nstat.py %s > /dev/null 2>&1 &" % (self.remote_server_main_dir, log_file)
            print("%s run client stats: %s" % (client[0], cmd))
            self.exe(client, cmd, True)
                
        time_to_run = 50
        time_to_sleep = 0
        i=0
        cc = 0
        for client in self.clients:
            for i in range(thread_per_client):
                server = self.servers[index]
                server_id = server[0].strip("netx")
                client_id = client[0].strip("netx")
                
                cmd = "iperf3 -c 10.1.0.%s -p %s -l 0 -t %d -O 8 -A %d > %s/run_tcp_client_%s_%d.log 2>&1 &" % (server_id, str(port_st), time_to_run, (i)%8, self.remote_server_log_dir, client[0], i)
                print("%s run tcp client: %s" % (client[0], cmd))
                self.exe(client, cmd, True)
                
                port_st = port_st + 1
                cc = cc + 1
                cc = cc % 8

            time.sleep(10)
        return

    def run_tcp_client(self, alg):        
        port_st = 10000
        index = 0
        log_id = 0
        for client in self.clients:
            server = self.servers[index]
            server_id = server[0].strip("netx")
            client_id = client[0].strip("netx")
            log_id = log_id + 1
            log_file = self.remote_server_res_dir + "/%s_%s.log" % (log_id, alg)
            cmd = "cd %s; cd host_code/simple_tcp; python nstat.py %s > /dev/null 2>&1 &" % (self.remote_server_main_dir, log_file)
            print("%s run client stats: %s" % (client[0], cmd))
            self.exe(client, cmd, True)
                
        time_to_run = 50
        time_to_sleep = 0
        i=0
        cc = 0
        for client in self.clients:
            for i in range(thread_per_client):
                server = self.servers[index]
                server_id = server[0].strip("netx")
                client_id = client[0].strip("netx")
                
                cmd = "iperf3 -c 10.1.0.%s -p %s -l 0 -t %d -O 8 -A %d > %s/run_tcp_client_%s_%d.log 2>&1 &" % (server_id, str(port_st), time_to_run, (i)%8, self.remote_server_log_dir, client[0], i)
                print("%s run tcp client: %s" % (client[0], cmd))
                self.exe(client, cmd, True)
                
                port_st = port_st + 1
                cc = cc + 1
                cc = cc % 8

            time.sleep(10)
        return

    def run_tcp_server(self):
        port_st = 10000
        cc = 0
        for client in self.clients:
            for server in self.servers:
                for i in range(thread_per_client):
                    client_id = client[0].strip("netx")
                    server_id = server[0].strip("netx")
                    # cmd = "cd %s; cd host_code/simple_tcp; python throughput.py -s %s > %s/run_tcp_server_%s_%d.log 2>&1 &" % (self.remote_server_main_dir, str(port_st), self.remote_server_res_dir, client_id, i)
                    
                    cmd = "iperf3 -s -p %s -i 0 -D -A %d" % (str(port_st), port_st%8)
                    print("%s run tcp server: %s" % (server[0], cmd))
                    self.exe(server, cmd, True)
                    port_st = port_st + 1
                    cc = cc + 1
                    cc = cc % 8
                    # time.sleep(8)
        return

    def run_host(self):
        self.run_server()
        self.run_client()

    def run_aifo(self):
        sde_dir = self.remote_switch_sde_dir
        ## run switch
        run_aifod = sde_dir + "run_switchd.sh"
        cmd = "cd %s;source ./set_sde.bash;%s -p %s > %s/run_switchd.log 2>&1 &" % (sde_dir, run_aifod,
            self.program_name, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)

        ## run ptf_test 
        run_ptf_test = sde_dir + "run_p4_tests.sh"
        ports_map = self.remote_switch_ptf_dir + "ports.json"
        target_mode = "hw"
        cmd = "cd %s;source ./set_sde.bash;%s -t %s -p %s -f %s --target %s > %s/run_ptf_test.log 2>&1 &" % (sde_dir, run_ptf_test,
            self.remote_switch_ptf_dir, self.program_name, ports_map, target_mode, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)
        return

    def run_sppifo(self):
        sde_dir = self.remote_switch_sde_dir
        ## run switch 
        run_sppifod = sde_dir + "run_switchd.sh"
        cmd = "cd %s;source ./set_sde.bash;%s -p %s > %s/run_switchd.log 2>&1 &" % (sde_dir, run_sppifod,
            self.sppifo_name, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)

        ## run ptf_test
        run_ptf_test = sde_dir + "run_p4_tests.sh"
        ports_map = self.remote_switch_sppifo_ptf_dir + "ports.json"
        target_mode = "hw"
        cmd = "cd %s;source ./set_sde.bash;%s -t %s -p %s -f %s --target %s > %s/run_ptf_test.log 2>&1 &" % (sde_dir, run_ptf_test,
            self.remote_switch_sppifo_ptf_dir, self.sppifo_name, ports_map, target_mode, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)
        return
        

    def run_simple_switch(self):
        sde_dir = self.remote_switch_sde_dir
        ## run switch
        run_swd = sde_dir + "run_switchd.sh"
        cmd = "cd %s;source ./set_sde.bash;%s -p %s > %s/run_simple_switch_switchd.log 2>&1 &" % (sde_dir, run_swd,
            self.simple_switch_name, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)

        ## run ptf_test 
        run_ptf_test = sde_dir + "run_p4_tests.sh"
        ports_map = self.remote_switch_simple_switch_ptf_dir + "ports.json"
        target_mode = "hw"
        cmd = "cd %s;source ./set_sde.bash;%s -t %s -p %s -f %s --target %s > %s/run_simple_switch_ptf_test.log 2>&1 &" % (sde_dir, run_ptf_test,
            self.remote_switch_simple_switch_ptf_dir, self.simple_switch_name, ports_map, target_mode, self.remote_switch_log_dir)
        print(cmd)
        self.exe(self.switch, cmd, True)
        return

    def run_udp(self):
        self.kill_all()
        time.sleep(10)
        self.run_aifo()
        time.sleep(80)
        self.send_workers()
        self.run_server("aifo")
        time.sleep(10)
        self.run_client()
        time.sleep(30)
        self.grab_result()
        self.kill_host()
        return

    def run_udp_sppifo(self):
        self.kill_all()
        time.sleep(10)
        self.run_sppifo()
        time.sleep(80)
        self.run_server("sppifo")
        time.sleep(10)
        self.run_client()
        time.sleep(30)
        self.grab_result()
        self.kill_host()
        return

    def run_udp_sw(self):
        self.kill_all()
        time.sleep(10)
        self.run_simple_switch()
        time.sleep(60)
        self.run_server("fifo")
        time.sleep(10)
        self.run_client()
        time.sleep(30)
        self.grab_result()
        self.kill_host()
        return

    def run_tcp(self):
        self.kill_all()
        time.sleep(10)
        self.run_aifo()
        time.sleep(80)
        self.send_workers()
        self.run_tcp_server()
        time.sleep(1)
        self.run_tcp_client("aifo")
        print("sleep for 40s...")
        time.sleep(50)
        self.kill_all()
        self.grab_result()
        return

    def run_tcp_sppifo(self):
        self.kill_all()
        time.sleep(10)
        self.run_sppifo()
        time.sleep(80)
        self.run_tcp_server()
        time.sleep(1)
        self.run_tcp_client("sppifo")
        print("sleep for 50s...")
        time.sleep(50)
        self.kill_all()
        self.grab_result()
        return

    def run_tcp_sw(self):
        self.kill_all()
        time.sleep(10)
        self.run_simple_switch()
        time.sleep(50)
        self.run_tcp_server()
        time.sleep(1)
        self.run_tcp_client("fifo")
        print("sleep for 60s...")
        time.sleep(60)
        self.kill_all()
        self.grab_result()
        return

    def setup_dpdk(self):
        self.kill_arp_host()
        dpdk_dir = self.remote_server_dpdk_dir

        cmd_eth_down = "ifconfig enp5s0f0 down > %s/eth_down.log 2>&1 &" % (self.remote_server_log_dir)
        
        for client in self.clients:
            cmd_setup_dpdk = "export passwd=%s;source ~/.bash_profile;echo $RTE_SDK;sh %s/tools.sh setup_dpdk > %s/setup_dpdk.log 2>&1 &" % (self.passwd[client[0]], dpdk_dir, self.remote_server_log_dir)
            print("%s run eth_down: %s" % (client[0], cmd_eth_down))
            self.sudo_exe(client, cmd_eth_down, True)
            print("%s run setup_dpdk: %s" % (client[0], cmd_setup_dpdk))
            self.exe(client, cmd_setup_dpdk, True)

        for server in self.servers:
            cmd_setup_dpdk = "export passwd=%s;source ~/.bash_profile;echo $RTE_SDK;sh %s/tools.sh setup_dpdk > %s/setup_dpdk.log 2>&1 &" % (self.passwd[server[0]], dpdk_dir, self.remote_server_log_dir)
            print("%s run eth_down: %s" % (server[0], cmd_eth_down))
            self.sudo_exe(server, cmd_eth_down, True)
            print("%s run setup_dpdk: %s" % (server[0], cmd_setup_dpdk))
            self.exe(server, cmd_setup_dpdk, True)
        return

    def unbind_dpdk(self):
        dpdk_dir = self.remote_server_dpdk_dir
        cmd_eth_up = "ifconfig enp5s0f0 up > %s/eth_up.log 2>&1 &" % (self.remote_server_log_dir)

        for client in self.clients:
            cmd_unbind_dpdk = "export passwd=%s;source ~/.bash_profile;echo $RTE_SDK;sh %s/tools.sh unbind_dpdk > %s/unbind_dpdk.log 2>&1 &" % (self.passwd[client[0]], dpdk_dir, self.remote_server_log_dir)
            print("%s run unbind_dpdk" % (client[0]))
            self.exe(client, cmd_unbind_dpdk, True)
            print("%s run eth_up: %s" % (client[0], cmd_eth_up))
            self.sudo_exe(client, cmd_eth_up, True)

        for server in self.servers:
            cmd_unbind_dpdk = "export passwd=%s;source ~/.bash_profile;echo $RTE_SDK;sh %s/tools.sh unbind_dpdk > %s/unbind_dpdk.log 2>&1 &" % (self.passwd[server[0]], dpdk_dir, self.remote_server_log_dir)
            print("%s run unbind_dpdk" % (server[0]))
            self.exe(server, cmd_unbind_dpdk, True)
            print("%s run eth_up: %s" % (server[0], cmd_eth_up))
            self.sudo_exe(server, cmd_eth_up, True)
        return

    def get_tput(self):
        for client in self.clients: 
            for i in range(thread_per_client):
                client_id = client[0].strip("netx")
                cmd = "cat ~/zhuolong/exp/aifo/logs/run_tcp_client_%s_%d.log | grep sender" % (client[0], i)
                print("%s get tput" % (client[0]))
                self.exe(client, cmd, True)
        return

    def get_kernel(self):
        for client in self.clients: 
            client_id = client[0].strip("netx")
            cmd = "uname -r"
            print("%s get kernel version " % (client[0]))
            self.exe(client, cmd, True)
        for server in self.servers: 
            server_id = server[0].strip("netx")
            cmd = "uname -r"
            print("%s get kernel version " % (server[0]))
            self.exe(server, cmd, True)
        return

    def reboot_host(self):
        cmd = "reboot > %s/reboot.log 2>&1 &" % (self.remote_server_log_dir)
        for client in self.clients:
            print("%s run eth_down: %s" % (client[0], cmd))
            self.sudo_exe(client, cmd, True)
        
        for server in self.servers:
            print("%s run eth_down: %s" % (server[0], cmd))
            self.sudo_exe(client, cmd, True)


    def grab_result(self):
        for client in self.client_names:
            cmd = "rsync -r %s@%s:%s %s" % (self.to_username(client), self.to_hostname(client), self.remote_server_res_dir, self.local_res_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
        
        for server in self.server_names:
            cmd = "rsync -r %s@%s:%s %s" % (self.to_username(server), self.to_hostname(server), self.remote_server_res_dir, self.local_res_dir)
            print(cmd)
            subprocess.call(cmd, shell = True)
        return

    def clean_result(self):
        if ("aifo" in self.remote_server_res_dir):
            cmd = "rm -rf  %s/* > /dev/null  2>&1 & " % (self.remote_server_res_dir)
            for client in self.clients:
                print("%s deleting the result files: %s" % (client[0], cmd))
                self.sudo_exe(client, cmd, True)
            for server in self.servers:
                print("%s deleting the result files: %s" % (server[0], cmd))
                self.sudo_exe(server, cmd, True)
        return

    def send_workers(self):
        for worker in self.worker:
            cmd = "cd %s; python2.7 worker.py 10.1.0.12 144 0 5; python2.7 worker.py 10.1.0.12 144 0 5; python2.7 worker.py 10.1.0.12 144 0 5; python2.7 worker.py 10.1.0.12 144 0 5; python2.7 worker.py 10.1.0.12 144 0 5; python2.7 worker.py 10.1.0.12 144 0 5 > %s/send_workers.log 2>&1 &" % (self.remote_server_worker_dir, self.remote_server_log_dir)
            print(cmd)
            self.exe(worker, cmd, True)
        return

def print_usage():
    ### TODO: rewrite the usage
    prRed("Usage")
    prRed("  python console.py init_sync_(host, switch)")
    prRed("  python console.py sync_(host, trace, switch, all)")
    prRed("  python console.py compile_(host, switch, all)")
    prRed("  python console.py run_(client, server, aifo, host, all)")
    prRed("  python console.py setup_dpdk")
    prRed("  python console.py reboot_host")
    prRed("  python console.py grab_result")
    prRed("  python console.py clean_result")
    # prRed("  console.py benchmark (e.g. micro_bm_s, micro_bm_x, micro_bm_cont, mem_man, mem_size, think_time, run_tpcc, run_tpcc_ms)")
    prRed("  python console.py [run_udp_aifo | run_udp_sw | run_udp_sppifo | run_tcp_aifo | run_tcp_sw | run_tcp_sppifo]")
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print_usage()
        sys.exit(0)

    serverNum = 1

    nl_console = CSFQConsole(
                          ["netx7", "netx8", "netx9", "netx11"], 
                          ["netx12"],
                          ["netx1"],
                          "netxy")
    
    nl_options = {
        "init_sync_host": nl_console.init_sync_host,
        "init_sync_switch": nl_console.init_sync_switch,
        "sync_host": nl_console.sync_host,
        "sync_switch": nl_console.sync_switch,
        "sync_all": nl_console.sync_all,
        "compile_host": nl_console.compile_host,
        "compile_aifo": nl_console.compile_aifo,
        "compile_all": nl_console.compile_all,
        "compile_sppifo": nl_console.compile_sppifo,
        "compile_fifo": nl_console.compile_sw,
        "run_client": nl_console.run_client, 
        "run_server": nl_console.run_server, 
        "run_aifo": nl_console.run_aifo,
        # "run_all": nl_console.run_all,
        "kill_host": nl_console.kill_host,
        "kill_switch": nl_console.kill_switch,
        "kill_all": nl_console.kill_all,
        "setup_dpdk": nl_console.setup_dpdk,
        "unbind_dpdk": nl_console.unbind_dpdk,
        "reboot_host": nl_console.reboot_host,
        "grab_result": nl_console.grab_result,
        "clean_result": nl_console.clean_result,
        "run_host": nl_console.run_host,
        "run_simple_switch": nl_console.run_simple_switch,
        "run_tcp_client": nl_console.run_tcp_client,
        "run_tcp_server": nl_console.run_tcp_server,
        "set_arp": nl_console.setup_arp,
        "kill_arp": nl_console.kill_arp,
        "get_kernel": nl_console.get_kernel,
        "get_tput": nl_console.get_tput,
        "run_udp_aifo": nl_console.run_udp,
        "run_udp_fifo": nl_console.run_udp_sw,
        "run_udp_sppifo": nl_console.run_udp_sppifo,
        "run_tcp_aifo": nl_console.run_tcp,
        "run_tcp_fifo": nl_console.run_tcp_sw,
        "run_tcp_sppifo": nl_console.run_tcp_sppifo,
        "set_tc": nl_console.setup_tc,
        "clear_tc": nl_console.clear_tc,
        "worker": nl_console.send_workers,
    }
    if sys.argv[1] in nl_options:
        nl_options[sys.argv[1]]()
    else:
        print_usage()

        