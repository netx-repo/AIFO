import palettable
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shutil, os

colors = palettable.colorbrewer.qualitative.Paired_10.hex_colors

protocols = ["PIFO", "AIFO"]
q_lens = [100, 250, 375, 500]

#Make plots
fig, axs = plt.subplots(len(q_lens), len(protocols), figsize=(3*len(q_lens), 5*len(protocols)), sharex=True, sharey=True)
fig.tight_layout(pad=3.0)

for protocol_num, protocol in enumerate(protocols):
    for q_len_num, q_len in enumerate(q_lens):
        #Load all data
        path = "temp/aifo/aifo_evaluation/pFabric/web_search_workload_q_len_order/3600/{protocol}_C{q_len}/rank_at_10.log".format(protocol=protocol, q_len=q_len)
        print(path)
        accept_set = pd.read_csv(path, delim_whitespace=True, header=0)
        
        data = accept_set.rankx.to_numpy()
        flow_id = accept_set.flowid.to_numpy()
        #fig, axs[q_len_num, protocol_num] = plt.subplots(figsize=(5, 3))

        gap = 20
        stx = 10
        draw_data = np.append(data[0:stx+1], data[stx+1:60000-stx*gap+stx:gap])
        draw_id = np.append(flow_id[0:stx+1], flow_id[stx+1:60000-stx*gap+stx:gap])
        axs[q_len_num, protocol_num].set_xlim(0, 60000//gap)
        axs[q_len_num, protocol_num].set_xticks((range(0, 60000//gap + 1, 10000//gap)))
        axs[q_len_num, protocol_num].set_xticklabels(['0', '1', '2', '3', '4', '5', '6'])
        #axs[q_len_num, protocol_num].set_xlabel(r'Arriving order ($\times 10^4$)')
        axs[q_len_num, protocol_num].xaxis.set_ticks_position('bottom')
        #axs[q_len_num, protocol_num].set_ylabel(r'Rank ($\times 10^8$)')

        axs[q_len_num, protocol_num].set_ylim(ymin=0, ymax=105000000)
        axs[q_len_num, protocol_num].set_yticks((range(0, 100000001, 20000000)))
        axs[q_len_num, protocol_num].set_yticklabels(['0', '2', '4', '6', '8', '10'])
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

        axs[q_len_num, protocol_num].scatter(l_f_x, l_f_y, s[0:len(l_f_x)], color=colors[5], label='Large flow')
        axs[q_len_num, protocol_num].scatter(m_f_x, m_f_y, s[0:len(m_f_x)], color=colors[3], label='Medium flow')
        axs[q_len_num, protocol_num].scatter(s_f_x, s_f_y, s[0:len(s_f_x)], color=colors[1], label='Small flow')

        axs[q_len_num, protocol_num].set_title(f'{protocol} q_len={q_len}')
        
# set labels
plt.setp(axs[-1, :], xlabel=r'Arriving order ($\times 10^4$)')
plt.setp(axs[:, 0], ylabel=r'Rank ($\times 10^8$)')
        
#l = plt.legend(loc='best', numpoints=1, prop={'size':10}, labelspacing=0.20)
#l.set_frame_on(False)
#l.legendHandles[0]._sizes = [9]
#l.legendHandles[1]._sizes = [9]
#l.legendHandles[2]._sizes = [9]

plt.savefig('projects/aifo/plots/aifo_evaluation/selfDefinedFlows/figure18.png')


