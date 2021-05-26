import psutil
import time
from datetime import datetime
import os
import sys
def comp_bandwidth(new, old, interval):
    dRecv = new.bytes_recv - old.bytes_recv
    dSend = new.bytes_sent - old.bytes_sent
    return dRecv*8 / interval, dSend*8 / interval

def create_logfile():
    log_folder = "./logs/netll"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    dt = datetime.fromtimestamp(time.time())
    timestamp = dt.strftime("%Y%m%d-%H%M%S")
    logfile = timestamp + '-net.log'
    return os.path.join(log_folder, logfile)

def sudo_exe(cmd):
    os.system("echo netpb0503 | sudo -S " + cmd)

def limit_rate(ratelimit):
    # cmd = "wondershaper enp5s0f0 " + str(int(ratelimit)) + " " + str(int(ratelimit))
    cmd = "tc qdisc replace dev enp5s0f0 root tbf rate " + str(int(ratelimit)) + "kbit latency 50ms burst " + str(int(ratelimit * 1.1))
    sudo_exe(cmd) 
    print("echo netpb0503 | sudo -S " + cmd)
    return

def main():
    interval = 0.1
    old_net_stat = psutil.net_io_counters()
    if len(sys.argv) > 1:
        # second arg as output log file
        logfile = sys.argv[1]
    else:
        logfile = create_logfile()
    ratelimit = 1000000 # 1Gbps
    limit_rate(ratelimit)
    # time.sleep(0.5)
    count = 0
    maxv = 0
    minv = 50000000000
    addition = 1000
    new_net_stat = psutil.net_io_counters(pernic=True)['enp5s0f0']
    old_net_stat = new_net_stat
    time.sleep(interval)
    new_net_stat = psutil.net_io_counters(pernic=True)['enp5s0f0']
    with open(logfile, 'w') as net_log:
        while True:
            # new_net_stat = psutil.net_io_counters()
            new_net_stat = psutil.net_io_counters(pernic=True)['enp5s0f0']
            old_net_stat = new_net_stat
            time.sleep(interval)
            new_net_stat = psutil.net_io_counters(pernic=True)['enp5s0f0']
            bandwidth = comp_bandwidth(new_net_stat, old_net_stat, interval)
            print(time.time(), 'Receiving(bit/sec)', bandwidth[0], 'Sending(bit/sec)', bandwidth[1], 'ratelimit', ratelimit)
            net_log.write("{}, {}, {}\n".format(time.time(), bandwidth[0], bandwidth[1]))
            net_log.flush()
            count += 1
            maxv = max(maxv, bandwidth[1])
            minv = min(minv, bandwidth[1])
            
            
            if (count == 10):
                count = 0
                # if (maxv - minv > 0.2 * maxv):
                if (minv == 0):
                    ratelimit = ratelimit * 0.9
                    addition = 0
                else:
                    if ratelimit < 10000:
                        ratelimit = ratelimit + ratelimit
                    else:
                        ratelimit = ratelimit * 1.05
                ratelimit += addition
                limit_rate(ratelimit)
                # time.sleep(0.5)
                maxv = 0
                minv = 50000000000
if __name__ == "__main__":
    main()