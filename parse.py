import sys, os, time, subprocess, random
import threading
from multiprocessing import Process
import matplotlib.pyplot as plt
import palettable
import numpy as np
import pandas as pd

colors = palettable.colorbrewer.qualitative.Paired_10.hex_colors
linestyles = ['-', '--', ":"]
plt.rc('font',**{'size': 16, 'family': 'Arial' })
plt.rc('pdf',fonttype = 42)

class TestbedResultParser:
    def __init__(self, num_clients):
        self.num_clients = num_clients
        return

    def parse_udp_results(self, alg):
        fig, ax = plt.subplots(figsize=(5, 3))
        
        f_list = [[], [], [], []]
        for x in range(self.num_clients):
            cmd = "cat aifo_testbed/results/server_run_%s.log | grep 'rx:' | grep 'core %d' | awk -F [' |\t']+ '{print $7}'" % (alg, x + 1)
            # print(cmd)
            out_tput = subprocess.check_output(cmd.encode(), shell=True).decode().strip('\n').split('\n')
            res_tput = []
            for tput in out_tput:
                res_tput.append(float(tput))
            # print "plot_udp_" + alg + "_" + str(x+1) + "=", res_tput
            f_list[x] = res_tput[40:]
        for func in f_list:
            for i in range(len(func)):
                func[i] = func[i] / 1000000000.0
        ax.set_xlim(0, 20)
        ax.set_xticks(np.arange(0, 21, step=5))
        ax.set_xlabel('Time (s)')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Throughput (Gbps)')
        ax.set_ylim(ymin=0, ymax=40)
        ax.yaxis.set_ticks_position('left')

        min_len = min(min(len(f_list[0]), len(f_list[1])), min(len(f_list[2]), len(f_list[3])))
        print(min_len)
        min_len = 160


            
        idx = [i+1 for i in range(min_len)]
        for i in range(min_len):
            idx[i] = idx[i] * 20.0 / (min_len)
            
        plt.plot(idx, f_list[0][0:min_len], label='Flow 1',\
        color=colors[1], marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, f_list[1][0:min_len], label='Flow 2',\
        color=colors[3], marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, f_list[2][0:min_len], label='Flow 3',\
        color=colors[5], marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, f_list[3][0:min_len], label='Flow 4',\
        color=colors[7], marker='o', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        l = plt.legend(loc='upper right', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        # plt.show()
        plt.savefig("figs/Eval_udp_%s.pdf" % (alg), bbox_inches='tight')
        return

    def parse_tcp_results(self, alg):
        fig, ax = plt.subplots(figsize=(5, 3))
        f_list = [[], [], [], []]

        for x in range(self.num_clients):
            cmd = "cat aifo_testbed/results/%d_%s.log | grep -v '-' | awk -F [',']+ '{print $3}'" % (x+1, alg)
            out_tput = subprocess.check_output(cmd.encode(), shell=True).decode().strip('\n').split('\n')
            res_tput = []
            for tput in out_tput:
                res_tput.append(float(tput))
            f_list[x] = res_tput[4:]    
            # print("plot_tcp_" + alg + "_" + str(x+1) + "=", res_tput)

        for func in f_list:
            for i in range(len(func)):
                func[i] = func[i] / 1000000000.0
        for func in f_list:
            for i in range(len(func)):
                if (i>3) and (i<len(func) - 3):
                    func[i] = (func[i-1] + func[i] + func[i+1] + func[i-2] + func[i+2] + func[i-3] + func[i+3]) / 7.0

        ax.set_xlim(0, 20)
        ax.set_xticks(np.arange(0, 21, step=5))
        ax.set_xlabel('Time (s)')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Throughput (Gbps)')
        ax.set_ylim(ymin=0, ymax=40)
        ax.yaxis.set_ticks_position('left')

        min_len = min(min(len(f_list[0]), len(f_list[1])), min(len(f_list[2]), len(f_list[3])))
        print(min_len)
        min_len = 200


            
        idx = [i+1 for i in range(min_len)]
        for i in range(min_len):
            idx[i] = idx[i] * 20.0 / (min_len)
            
        plt.plot(idx, f_list[0][0:min_len], label='Flow 1',\
        color=colors[1], marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, f_list[1][0:min_len], label='Flow 2',\
        color=colors[3], marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, f_list[2][0:min_len], label='Flow 3',\
        color=colors[5], marker='>', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, f_list[3][0:min_len], label='Flow 4',\
        color=colors[7], marker='o', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        l = plt.legend(loc='upper right', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        # plt.show()
        plt.savefig("figs/Eval_tcp_%s.pdf" % (alg), bbox_inches='tight')

        return

class SimulationResultParser:
    def __init__(self):
        # compare with other solutions (tcp, dctcp, pifo, sppifo)
        self.all_comparison_less_100kb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload/pFabric_less_100KB_mean_fct_ms.dat'
        self.all_comparison_less_100kb_99th_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload/pFabric_less_100KB_99th_fct_ms.dat'
        self.all_comparison_geq_1mb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload/pFabric_geq_1MB_mean_fct_ms.dat'

        # queue length
        self.queue_length_less_100kb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len/pFabric_less_100KB_mean_fct_ms.dat'
        self.queue_length_less_100kb_99th_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len/pFabric_less_100KB_99th_fct_ms.dat'
        self.queue_length_geq_1mb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len/pFabric_geq_1MB_mean_fct_ms.dat'
        self.queue_length_less_100kb_mean_fct_14_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_1_4/pFabric_less_100KB_mean_fct_ms.dat'
        self.queue_length_less_100kb_99th_fct_14_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_1_4/pFabric_less_100KB_99th_fct_ms.dat'
        self.queue_length_geq_1mb_mean_fct_14_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_1_4/pFabric_geq_1MB_mean_fct_ms.dat'

        # window length
        self.window_length_less_100kb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_w_sr/pFabric_less_100KB_mean_fct_ms.dat'
        self.window_length_less_100kb_99th_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_w_sr/pFabric_less_100KB_99th_fct_ms.dat'
        self.window_length_geq_1mb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_w_sr/pFabric_geq_1MB_mean_fct_ms.dat'

        # accepting set
        self.accept_set_aifo_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/selfDefinedFlows/AIFO.dat'
        self.accept_set_tcp_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/selfDefinedFlows/TCP.dat'
        self.accept_set_pifo_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/selfDefinedFlows/PIFO.dat'
        self.accept_set_sppifo_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/selfDefinedFlows/SPPIFO.dat'

        # fairness
        self.fairness_less_100KB_mean_fct_ms_32_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/fairness/web_search_workload/fairness_less_100KB_mean_fct_ms_32.dat'
        self.fairness_split_mean_fct_ms_32_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/fairness/web_search_workload/fairness_split_mean_fct_ms_32.dat'

        # K
        self.k_less_100kb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_C_K/pFabric_less_100KB_mean_fct_ms.dat'
        self.k_less_100kb_99th_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_C_K/pFabric_less_100KB_99th_fct_ms.dat'
        self.k_geq_1mb_mean_fct_name = f'aifo_simulation/java-code/projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_C_K/pFabric_geq_1MB_mean_fct_ms.dat'

        return
    
    def fig7a(self):
        all_comparison_less_100kb_mean_fct = pd.read_csv(self.all_comparison_less_100kb_mean_fct_name, delim_whitespace=True, header=0)

        data = all_comparison_less_100kb_mean_fct
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        fct_toy = [0.12314378469520104, 0.14510715820368886, 0.1614159276962242, 0.16760888058756726, 0.16881316741919622, 0.16757103053953173, 0.1673070446649907]


        plt.plot(idx, data.TCP, label='TCP', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.DCTCP, label='DCTCP', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.AIFO, label='AIFO', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.SPPIFO, label='SP-PIFO', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.PIFO, label='PIFO', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)


        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=3)
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        # plt.show()
        plt.savefig("figs/7a.pdf", bbox_inches='tight')
        return

    def fig7b(self):
        all_comparison_less_100kb_99th_fct = pd.read_csv(self.all_comparison_less_100kb_99th_fct_name, delim_whitespace=True, header=0)

        data = all_comparison_less_100kb_99th_fct
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        fct_toy = [0.35055623999999974, 0.37653438000000017, 0.3854711899999998, 0.3799701599999994, 0.38856209999999974, 0.3943339, 0.4087696200000002]


        plt.plot(idx, data.TCP, label='TCP', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.DCTCP, label='DCTCP', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.AIFO, label='AIFO', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.SPPIFO, label='SP-PIFO', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.PIFO, label='PIFO', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=15)
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        # plt.show()
        plt.savefig("figs/7b.pdf", bbox_inches='tight')
        return

    def fig7c(self):
        all_comparison_geq_1mb_mean_fct = pd.read_csv(self.all_comparison_geq_1mb_mean_fct_name, delim_whitespace=True, header=0)

        data = all_comparison_geq_1mb_mean_fct
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.TCP, label='TCP', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.DCTCP, label='DCTCP', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.AIFO, label='AIFO', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.SPPIFO, label='SP-PIFO', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.PIFO, label='PIFO', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=120)
        ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        # plt.show()
        plt.savefig("figs/7c.pdf", bbox_inches='tight')
        return

    def fig8a(self):
        k_less_100kb_mean_fct = pd.read_csv(self.k_less_100kb_mean_fct_name, delim_whitespace=True, header=0)

        data = k_less_100kb_mean_fct

        fig, ax = plt.subplots(figsize=(5, 3))
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.TCP, label='FIFO', color=colors[6],\
                marker='o', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,1], label='k=0.1', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,2], label='k=0.3', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,3], label='k=0.7', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,4], label='k=0.9', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.PIFO, label='PIFO', color=colors[7],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=3)
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/8a.pdf", bbox_inches='tight')
        return
    
    def fig8b(self):
        k_less_100kb_99th_fct = pd.read_csv(self.k_less_100kb_99th_fct_name, delim_whitespace=True, header=0)
        data = k_less_100kb_99th_fct

        fig, ax = plt.subplots(figsize=(5, 3))
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]


        plt.plot(idx, data.TCP, label='FIFO', color=colors[6],\
                marker='o', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,1], label='k=0.1', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,2], label='k=0.3', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,3], label='k=0.7', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,4], label='k=0.9', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.PIFO, label='PIFO', color=colors[7],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)


        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=15)
        # ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/8b.pdf", bbox_inches='tight')
        return

    def fig8c(self):
        k_geq_1mb_mean_fct = pd.read_csv(self.k_geq_1mb_mean_fct_name, delim_whitespace=True, header=0)
        data = k_geq_1mb_mean_fct

        fig, ax = plt.subplots(figsize=(5, 3))
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.TCP, label='FIFO', color=colors[6],\
                marker='o', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,1], label='k=0.1', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,2], label='k=0.3', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,3], label='k=0.7', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,4], label='k=0.9', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.PIFO, label='PIFO', color=colors[7],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=120)
        ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/8c.pdf", bbox_inches='tight')
        return

    def fig9a(self):
        window_length_less_100kb_mean_fct = pd.read_csv(self.window_length_less_100kb_mean_fct_name, delim_whitespace=True, header=0)
        data = window_length_less_100kb_mean_fct
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.W1000_SR1, label='win_len=1000, sample_rate=1', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,3], label='win_len=100, sample_rate=0.1', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,1], label='win_len=20, sample_rate=0.02', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,2], label='win_len=20, sample_rate=1', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        
        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=0.2)
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='lower center', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/9a.pdf", bbox_inches='tight')
        return

    def fig9b(self):
        window_length_less_100kb_99th_fct = pd.read_csv(self.window_length_less_100kb_99th_fct_name, delim_whitespace=True, header=0)
        data = window_length_less_100kb_99th_fct
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.W1000_SR1, label='win_len=1000, sample_rate=1', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,3], label='win_len=100, sample_rate=0.1', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,1], label='win_len=20, sample_rate=0.02', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,2], label='win_len=20, sample_rate=1', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        
        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=2)
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper center', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/9b.pdf", bbox_inches='tight')
        return

    def fig9c(self):
        window_length_geq_1mb_mean_fct = pd.read_csv(self.window_length_geq_1mb_mean_fct_name, delim_whitespace=True, header=0)
        data = window_length_geq_1mb_mean_fct
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.W1000_SR1, label='win_len=1000, sample_rate=1', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,3], label='win_len=100, sample_rate=0.1', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,1], label='win_len=20, sample_rate=0.02', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.iloc[:,2], label='win_len=20, sample_rate=1', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        
        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=80)
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper center', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/9c.pdf", bbox_inches='tight')
        return

    def fig10a(self):
        queue_length_less_100kb_mean_fct_14 = pd.read_csv(self.queue_length_less_100kb_mean_fct_14_name, delim_whitespace=True, header=0)
        data = queue_length_less_100kb_mean_fct_14
        fig, ax = plt.subplots(figsize=(5, 3))
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.C500, label='q_len=500', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C100, label='q_len=100', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C50, label='q_len=50', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C20, label='q_len=20', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C10, label='q_len=10', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=15)
        # ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/10a.pdf", bbox_inches='tight')
        return

    def fig10b(self):
        queue_length_geq_1mb_mean_fct_14 = pd.read_csv(self.queue_length_geq_1mb_mean_fct_14_name, delim_whitespace=True, header=0)
        data = queue_length_geq_1mb_mean_fct_14
        fig, ax = plt.subplots(figsize=(5, 3))
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.C500, label='q_len=500', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C100, label='q_len=100', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C50, label='q_len=50', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C20, label='q_len=20', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C10, label='q_len=10', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=150)
        # ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/10b.pdf", bbox_inches='tight')
        return

    def fig11a(self):
        queue_length_less_100kb_mean_fct = pd.read_csv(self.queue_length_less_100kb_mean_fct_name, delim_whitespace=True, header=0)
        data = queue_length_less_100kb_mean_fct
        fig, ax = plt.subplots(figsize=(5, 3))
        # print(data.C200)
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.C500, label='q_len=500', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C100, label='q_len=100', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C50, label='q_len=50', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C20, label='q_len=20', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C10, label='q_len=10', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=1)
        # ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        # plt.show()
        plt.savefig("figs/11a.pdf", bbox_inches='tight')
        return

    def fig11b(self):
        queue_length_geq_1mb_mean_fct = pd.read_csv(self.queue_length_geq_1mb_mean_fct_name, delim_whitespace=True, header=0)

        data = queue_length_geq_1mb_mean_fct
        fig, ax = plt.subplots(figsize=(5, 3))
        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.C500, label='q_len=500', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C100, label='q_len=100', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C50, label='q_len=50', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C20, label='q_len=20', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.C10, label='q_len=10', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=50)
        # ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':14}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/11b.pdf", bbox_inches='tight')
        return

    def fig12a(self):
        accept_set_tcp = pd.read_csv(self.accept_set_tcp_name, delim_whitespace=True, header=0)
        data = accept_set_tcp.rankx.to_numpy()
        flow_id = accept_set_tcp.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 20
        stx = 10
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 60000//gap)
        ax.set_xticks((range(0, 60000//gap + 1, 10000//gap)))
        ax.set_xticklabels(['0', '1', '2', '3', '4', '5', '6'])
        ax.set_xlabel(r'Arriving order ($\times 10^4$)')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^8$)')

        ax.set_ylim(ymin=0, ymax=105000000)
        ax.set_yticks((range(0, 100000001, 20000000)))
        ax.set_yticklabels(['0', '2', '4', '6', '8', '10'])
        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])
        plt.scatter(l_f_x, l_f_y, s[0:len(l_f_x)], color=colors[5], label='Large flow')
        plt.scatter(m_f_x, m_f_y, s[0:len(m_f_x)], color=colors[3], label='Medium flow')
        plt.scatter(s_f_x, s_f_y, s[0:len(s_f_x)], color=colors[1], label='Small flow')
        l = plt.legend(loc='center right', numpoints=1, prop={'size':15}, labelspacing=0.36)
        l.set_frame_on(False)
        l.legendHandles[0]._sizes = [9]
        l.legendHandles[1]._sizes = [9]
        l.legendHandles[2]._sizes = [9]
        plt.savefig("figs/12a.pdf", bbox_inches='tight')
        return

    def fig12b(self):
        accept_set_pifo = pd.read_csv(self.accept_set_pifo_name, delim_whitespace=True, header=0)
        data = accept_set_pifo.rankx.to_numpy()
        flow_id = accept_set_pifo.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 20
        stx = 10
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 60000//gap)
        ax.set_xticks((range(0, 60000//gap + 1, 10000//gap)))
        ax.set_xticklabels(['0', '1', '2', '3', '4', '5', '6'])
        ax.set_xlabel(r'Arriving order ($\times 10^4$)')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^8$)')

        ax.set_ylim(ymin=0, ymax=105000000)
        ax.set_yticks((range(0, 100000001, 20000000)))
        ax.set_yticklabels(['0', '2', '4', '6', '8', '10'])
        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])

        plt.scatter(l_f_x, l_f_y, s[0:len(l_f_x)], color=colors[5], label='Large flow')
        plt.scatter(m_f_x, m_f_y, s[0:len(m_f_x)], color=colors[3], label='Medium flow')
        plt.scatter(s_f_x, s_f_y, s[0:len(s_f_x)], color=colors[1], label='Small flow')
        l = plt.legend(loc='center right', numpoints=1, prop={'size':15}, labelspacing=0.36)
        l.set_frame_on(False)
        l.legendHandles[0]._sizes = [9]
        l.legendHandles[1]._sizes = [9]
        l.legendHandles[2]._sizes = [9]
        plt.savefig("figs/12b.pdf", bbox_inches='tight')
        return

    def fig12c(self):
        accept_set_sppifo = pd.read_csv(self.accept_set_sppifo_name, delim_whitespace=True, header=0)
        data = accept_set_sppifo.rankx.to_numpy()
        flow_id = accept_set_sppifo.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 20
        stx = 10
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 60000//gap)
        ax.set_xticks((range(0, 60000//gap + 1, 10000//gap)))
        ax.set_xticklabels(['0', '1', '2', '3', '4', '5', '6'])
        ax.set_xlabel(r'Arriving order ($\times 10^4$)')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^8$)')

        ax.set_ylim(ymin=0, ymax=105000000)
        ax.set_yticks((range(0, 100000001, 20000000)))
        ax.set_yticklabels(['0', '2', '4', '6', '8', '10'])
        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])
        plt.scatter(l_f_x, l_f_y, s[0:len(l_f_x)], color=colors[5], label='Large flow')
        plt.scatter(m_f_x, m_f_y, s[0:len(m_f_x)], color=colors[3], label='Medium flow')
        plt.scatter(s_f_x, s_f_y, s[0:len(s_f_x)], color=colors[1], label='Small flow')
        l = plt.legend(loc='center right', numpoints=1, prop={'size':15}, labelspacing=0.36)
        l.set_frame_on(False)
        l.legendHandles[0]._sizes = [9]
        l.legendHandles[1]._sizes = [9]
        l.legendHandles[2]._sizes = [9]
        plt.savefig("figs/12c.pdf", bbox_inches='tight')
        return

    def fig12d(self):
        accept_set_aifo = pd.read_csv(self.accept_set_aifo_name, delim_whitespace=True, header=0)
        data = accept_set_aifo.rankx.to_numpy()
        flow_id = accept_set_aifo.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 20
        stx = 10
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])
        ax.set_xlim(0, 60000//gap)
        ax.set_xticks((range(0, 60000//gap + 1, 10000//gap)))
        ax.set_xticklabels(['0', '1', '2', '3', '4', '5', '6'])
        ax.set_xlabel(r'Arriving order ($\times 10^4$)')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^8$)')

        ax.set_ylim(ymin=0, ymax=105000000)
        ax.set_yticks((range(0, 100000001, 20000000)))
        ax.set_yticklabels(['0', '2', '4', '6', '8', '10'])
        s = [6 for n in range(60000 // gap)]
        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])

        plt.scatter(l_f_x, l_f_y, s[0:len(l_f_x)], color=colors[5], label='Large flow')
        plt.scatter(m_f_x, m_f_y, s[0:len(m_f_x)], color=colors[3], label='Medium flow')
        plt.scatter(s_f_x, s_f_y, s[0:len(s_f_x)], color=colors[1], label='Small flow')
        l = plt.legend(loc='center right', numpoints=1, prop={'size':15}, labelspacing=0.36)
        l.set_frame_on(False)
        l.legendHandles[0]._sizes = [9]
        l.legendHandles[1]._sizes = [9]
        l.legendHandles[2]._sizes = [9]
        plt.savefig("figs/12d.pdf", bbox_inches='tight')
        return

    def fig13a(self):
        fairness_less_100KB_mean_fct_ms_32 = pd.read_csv(self.fairness_less_100KB_mean_fct_ms_32_name, delim_whitespace=True, header=0)
        data = fairness_less_100KB_mean_fct_ms_32
        fig, ax = plt.subplots(figsize=(5, 3))

        idx = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        plt.plot(idx, data.TCP, label='TCP', color=colors[6],\
                marker='*', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.DCTCP, label='DCTCP', color=colors[9],\
                marker='D', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.AIFOWFQ, label='AIFO', color=colors[5],\
                marker='P', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.SPPIFOWFQ_32, label='SPPIFO', color=colors[3],\
                marker='^', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)
        plt.plot(idx, data.AFQ_32, label='AFQ', color=colors[4],\
                marker='2', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        plt.plot(idx, data.PIFOWFQ_32, label='PIFO', color=colors[1],\
                marker='s', markersize=6, lw=1, linestyle=linestyles[0], clip_on=False)

        ax.set_xlim(0.2, 0.8)
        ax.set_xticks(([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
        ax.set_xlabel('Load')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.set_ylim(ymin=0, ymax=10)
        # ax.set_yticks(([0, 30, 60, 90, 120]))
        ax.yaxis.set_ticks_position('left')

        l = plt.legend(loc='upper left', numpoints=1, prop={'size':12}, labelspacing=0.36)
        l.set_frame_on(False)
        plt.savefig("figs/13a.pdf", bbox_inches='tight')
        return

    def fig13b(self):
        fig, ax = plt.subplots(figsize=(7, 4))
        fairness_split_mean_fct_ms_32 = pd.read_csv(self.fairness_split_mean_fct_ms_32_name, delim_whitespace=True, header=0)

        data= fairness_split_mean_fct_ms_32
        fct_tcp_mean = data.TCP.to_numpy()[::-1]
        fct_dctcp_mean = data.DCTCP.to_numpy()[::-1]
        fct_afq_mean = data.AFQ_32.to_numpy()[::-1]
        fct_sppifo_mean = data.SPPIFOWFQ_32.to_numpy()[::-1]
        fct_pifo_mean = data.PIFOWFQ_32.to_numpy()[::-1]
        fct_aifo_mean = data.AIFOWFQ.to_numpy()[::-1]

        fct_tcp_99th = data.TCP_9.to_numpy()[::-1]
        fct_dctcp_99th = data.DCTCP_9.to_numpy()[::-1]
        fct_afq_99th = data.AFQ_32_9.to_numpy()[::-1]
        fct_sppifo_99th = data.SPPIFOWFQ_32_9.to_numpy()[::-1]
        fct_pifo_99th = data.PIFOWFQ_32_9.to_numpy()[::-1]
        fct_aifo_99th = data.AIFOWFQ_9.to_numpy()[::-1]

        _mean_funcs = [fct_tcp_mean, fct_dctcp_mean, fct_afq_mean, fct_sppifo_mean, fct_pifo_mean,
                    fct_aifo_mean]
        _99th_funcs = [fct_tcp_99th, fct_dctcp_99th, fct_afq_99th, fct_sppifo_99th, fct_pifo_99th,
                    fct_aifo_99th]
       
        for x in range(len(_mean_funcs)):
            for i in range(len(_99th_funcs[x])):
                _99th_funcs[x][i] = _99th_funcs[x][i] - _mean_funcs[x][i]

        width = 0.1
        idx = [[0.1, 0.8, 1.5, 2.2, 2.9, 3.6, 4.3],
            [0.2, 0.9, 1.6, 2.3, 3.0, 3.7, 4.4],
            [0.3, 1.0, 1.7, 2.4, 3.1, 3.8, 4.5],
            [0.4, 1.1, 1.8, 2.5, 3.2, 3.9, 4.6],
            [0.5, 1.2, 1.9, 2.6, 3.3, 4.0, 4.7],
            [0.6, 1.3, 2.0, 2.7, 3.4, 4.1, 4.8]]

        xticks_idx = [0.35, 1.05, 1.75, 2.45, 3.15, 3.85, 4.55]
        # xticks_idx = idx[2]
        xticks = ["10K", "20K", "30K", "50K", "80K", "0.2M-1M", "$\geq$2M"]
        plt.xticks(xticks_idx, xticks)
        low = [0, 0, 0, 0, 0, 0, 0]
        ax.bar(idx[0], _mean_funcs[0], yerr=(low, _99th_funcs[0]), error_kw=dict(lw=1, capsize=3, capthick=1), width=width, align='center', ecolor=colors[6], capsize=10, label = "TCP", color=colors[6])
        ax.bar(idx[1], _mean_funcs[1], yerr=(low, _99th_funcs[1]), error_kw=dict(lw=1, capsize=3, capthick=1), width=width, align='center', ecolor=colors[9], capsize=10, label = "DCTCP", color=colors[9])
        ax.bar(idx[2], _mean_funcs[5], yerr=(low, _99th_funcs[5]), error_kw=dict(lw=1, capsize=3, capthick=1), width=width, align='center', ecolor=colors[1], capsize=10, label = "AIFO", color=colors[5])
        ax.bar(idx[4], _mean_funcs[2], yerr=(low, _99th_funcs[2]), error_kw=dict(lw=1, capsize=3, capthick=1), width=width, align='center', ecolor=colors[5], capsize=10, label = "AFQ", color=colors[4])
        ax.bar(idx[3], _mean_funcs[3], yerr=(low, _99th_funcs[3]), error_kw=dict(lw=1, capsize=3, capthick=1), width=width, align='center', ecolor=colors[3], capsize=10, label = "SPPIFO", color=colors[3])
        ax.bar(idx[5], _mean_funcs[4], yerr=(low, _99th_funcs[4]), error_kw=dict(lw=1, capsize=3, capthick=1), width=width, align='center', ecolor=colors[1], capsize=10, label = "PIFO", color=colors[1])

        l = plt.legend(numpoints=1, prop={'size':14}, loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=3)
        l.set_frame_on(False)

        ax.set_yscale('log')
        ax.set_xlabel('Flow size')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel('Flow completion time (ms)')
        ax.yaxis.set_ticks_position('left')

        plt.savefig("figs/13b.pdf", bbox_inches='tight')
        return

    def fig16a(self):
        accept_set_tcp = pd.read_csv(self.accept_set_tcp_name, delim_whitespace=True, header=0)
        data = accept_set_tcp.rankx.to_numpy()
        flow_id = accept_set_tcp.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 1
        stx = 0
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 300//gap)
        ax.set_xticks((range(0, 300//gap + 1, 50//gap)))
        ax.set_xlabel(r'Arriving order')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^5$)')

        ax.set_ylim(ymin=9500000, ymax=10010000)
        ax.set_yticks((range(9500000, 10000001, 100000)))
        ax.set_yticklabels(['95', '96', '97', '98', '99', '100'])

        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])
        plt.scatter(range(300), s_f_y[0:300], s[0:300], color=colors[1], label='Rank log')
        plt.savefig("figs/16a.pdf", bbox_inches='tight')
        return

    def fig16b(self):
        accept_set_pifo = pd.read_csv(self.accept_set_pifo_name, delim_whitespace=True, header=0)
        data = accept_set_pifo.rankx.to_numpy()
        flow_id = accept_set_pifo.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 1
        stx = 0
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 300//gap)
        ax.set_xticks((range(0, 300//gap + 1, 50//gap)))
        ax.set_xlabel(r'Arriving order')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^5$)')

        ax.set_ylim(ymin=9500000, ymax=10010000)
        ax.set_yticks((range(9500000, 10000001, 100000)))
        ax.set_yticklabels(['95', '96', '97', '98', '99', '100'])

        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])
        plt.scatter(s_f_x[0:300], s_f_y[0:300], s[0:300], color=colors[1], label='Rank log')
        plt.savefig("figs/16b.pdf", bbox_inches='tight')
        return

    def fig16c(self):
        accept_set_sppifo = pd.read_csv(self.accept_set_sppifo_name, delim_whitespace=True, header=0)
        data = accept_set_sppifo.rankx.to_numpy()
        flow_id = accept_set_sppifo.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 1
        stx = 0
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 300//gap)
        ax.set_xticks((range(0, 300//gap + 1, 50//gap)))
        ax.set_xlabel(r'Arriving order')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^5$)')

        ax.set_ylim(ymin=9500000, ymax=10010000)
        ax.set_yticks((range(9500000, 10000001, 100000)))
        ax.set_yticklabels(['95', '96', '97', '98', '99', '100'])

        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])
        plt.scatter(range(300), s_f_y[0:300], s[0:300], color=colors[1], label='Rank log')
        plt.savefig("figs/16c.pdf", bbox_inches='tight')
        return

    def fig16d(self):
        accept_set_aifo = pd.read_csv(self.accept_set_aifo_name, delim_whitespace=True, header=0)
        data = accept_set_aifo.rankx.to_numpy()
        flow_id = accept_set_aifo.flowid.to_numpy()
        fig, ax = plt.subplots(figsize=(5, 3))

        gap = 1
        stx = 0
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])

        ax.set_xlim(0, 300//gap)
        ax.set_xticks((range(0, 300//gap + 1, 50//gap)))
        ax.set_xlabel(r'Arriving order')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_ylabel(r'Rank ($\times 10^5$)')

        ax.set_ylim(ymin=9500000, ymax=10010000)
        ax.set_yticks((range(9500000, 10000001, 100000)))
        ax.set_yticklabels(['95', '96', '97', '98', '99', '100'])

        s = [6 for n in range(60000 // gap)]

        xcolors = []
        xlabels = []
        l_f_x = []
        l_f_y = []
        m_f_x = []
        m_f_y = []
        s_f_x = []
        s_f_y = []
        for i in range(60000 // gap):
            if draw_id[i]==0:
                l_f_x.append(i)
                l_f_y.append(draw_data[i])
            elif draw_id[i]==1:
                m_f_x.append(i)
                m_f_y.append(draw_data[i])
            else:
                s_f_x.append(i)
                s_f_y.append(draw_data[i])
        plt.scatter(range(300), s_f_y[0:300], s[0:300], color=colors[1], label='Rank log')
        plt.savefig("figs/16d.pdf", bbox_inches='tight')
        return


def print_usage():
    print("Usage:")
    print("  python parse.py udp [fifo|sppifo|aifo]")
    print("  python parse.py tcp [fifo|sppifo|aifo]")
    print("  python parse.py fig [fig_number (e.g., 7a)]")
    print("    - python parse.py fig 7a")

def main():
    num_clients = 4
    alg = None
    if (len(sys.argv) <= 2):
        print_usage()
        sys.exit(0)
    else:
        smpar = SimulationResultParser()
        if (sys.argv[1] == "fig"):
            fig_options = {
                "7a": smpar.fig7a,
                "7b": smpar.fig7b,
                "7c": smpar.fig7c,
                "8a": smpar.fig8a,
                "8b": smpar.fig8b,
                "8c": smpar.fig8c,
                "9a": smpar.fig9a,
                "9b": smpar.fig9b,
                "9c": smpar.fig9c,
                "10a": smpar.fig10a,
                "10b": smpar.fig10b,
                "11a": smpar.fig11a,
                "11b": smpar.fig11b,
                "12a": smpar.fig12a,
                "12b": smpar.fig12b,
                "12c": smpar.fig12c,
                "12d": smpar.fig12d,
                "13a": smpar.fig13a,
                "13b": smpar.fig13b,
                "16a": smpar.fig16a,
                "16b": smpar.fig16b,
                "16c": smpar.fig16c,
                "16d": smpar.fig16d,
            }
            if (sys.argv[2] in fig_options):
                fig_options[sys.argv[2]]()
            else:
                print_usage()
                sys.exit(0)
        else:
            if (sys.argv[2] == "fifo") or (sys.argv[2] == "sppifo") or (sys.argv[2] == "aifo"):
                alg = sys.argv[2]
            else:
                print_usage()
                sys.exit(0)
            

            par = TestbedResultParser(num_clients)

            if (sys.argv[1] == "udp"):
                par.parse_udp_results(alg)
            elif (sys.argv[1] == "tcp"):
                par.parse_tcp_results(alg)
            else:
                print_usage()
                sys.exit(0)

    return 

if __name__ == '__main__':
    main()