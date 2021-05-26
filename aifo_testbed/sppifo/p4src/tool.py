#!/usr/bin/python

from __future__ import print_function
import sys, os, time, subprocess, random

envir_path = "/home/hz/bf-sde-8.9.1-pg/bf-sde-8.9.1/"
# envir_path = "/home/zhuolong/bf-sde-8.2.2/"
p4_build = envir_path + "p4_build.sh"
run_tofino_model = envir_path + "run_tofino_model.sh"
run_switchd = envir_path + "run_switchd.sh"
run_p4_tests = envir_path + "run_p4_tests.sh"
set_sde = envir_path + "set_sde.bash"

sys_name = "simpleswitch"
target_mode = "hw"

def exe_cmd(cmd):
    #print "\t", cmd
    subprocess.call(cmd, shell=True)

def sync():
    exe_cmd("rsync -r * netx3:~/xinjin/p4src")

def compile(file_name):
    print("Try 'source ~/bf-sde-6.1.1.31/set_sde.bash' for debugging")
    exe_cmd("%s %s" % (p4_build, file_name))

def start_switch(p4_name):
    #exe_cmd("%s -p %s >tofino.log 2>&1 &" % (run_tofino_model, p4_name))
    print("%s -p %s" % (run_switchd, p4_name))
    exe_cmd("%s -p %s" % (run_switchd, p4_name))

def ptf_test(folder_name, lock_num):
    ports_map = folder_name + "/ports.json"
    print("%s -t %s -p %s -f %s --target %s" % (run_p4_tests, folder_name, sys_name, ports_map, target_mode))
    exe_cmd("%s -t %s -p %s -f %s --target %s --test-params=\"bm=\'x\';lk=\'%s\'\"" % (run_p4_tests, folder_name, sys_name, ports_map, target_mode, lock_num))

def stop_switch():
    exe_cmd("ps -ef | grep tofino | grep -v grep | " \
        "awk '{print $2}' | xargs sudo kill -9")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage")
        print("  tool.py sync")
        print("  tool.py init")
        print("  tool.py compile helloworld.p4")
        print("  tool.py start_switch helloworld")
        print("  tool.py stop_switch")
        print("  tool.py ptf_test helloworld/ptf-tests lock_num")
        sys.exit()

    if sys.argv[1] == "sync":
        sync()
    elif sys.argv[1] == "compile":
        compile(sys.argv[2])
    elif sys.argv[1] == "start_switch":
        start_switch(sys.argv[2])
    elif sys.argv[1] == "stop_switch":
        stop_switch()
    elif sys.argv[1] == "ptf_test":
        if (len(sys.argv) <=2):
            print("Not supported option)")
        else:
            ptf_test(sys.argv[2], sys.argv[3])
    else:
        print("Not supported option")
