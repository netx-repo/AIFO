import os

lambdas = [3600, 5200, 7000, 8900, 11100, 14150, 19000]
port = ["TCP", "DCTCP", "AFQ_32", "PIFOWFQ_32", "SPPIFOWFQ_32", "TOYWFQ"]


for x in lambdas:
    for y in port:
        cmdline = "python3 projects/sppifo/runs/sppifo_evaluation/fairness/web_search_workload/analyze_web_search.py temp/sppifo/sppifo_evaluation/fairness/web_search_workload/"+str(x)+"/"+y
        os.system(cmdline)