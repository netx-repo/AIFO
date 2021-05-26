import pandas as pd
import matplotlib.pyplot as plt
import numpy
import shutil, os

name = ["PIFO", "SPPIFO", "AIFO", "TCP"]

# move all temps into runs
for x in name:
    src_file = "temp/aifo/aifo_evaluation/pFabric/web_search_workload/3600/"+x+"/rank_at_10.log"
    dest_file = 'projects/aifo/plots/aifo_evaluation/selfDefinedFlows/' + x + ".dat"
    shutil.copy(src_file, dest_file)


# figure 12


# figure 16
for x in name:
    pat = "temp/aifo/aifo_evaluation/pFabric/web_search_workload/3600/"+x+"/rank_at_10.log"
    df = pd.read_csv(pat, delim_whitespace=True, header=0)
    plt.figure()
    plt.title(x)
    df = df[df['flowid']==2]                #select the smallest flow
    df = df.reset_index(drop=True)          #reset the index starting from 0
    plt.scatter(x=df.index[0:300], y=df.rankx[0:300])
    plt.savefig('projects/aifo/plots/aifo_evaluation/selfDefinedFlows/figure16/' +x+ '.png')
