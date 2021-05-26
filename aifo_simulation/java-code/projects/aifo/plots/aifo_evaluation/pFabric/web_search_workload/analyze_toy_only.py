#!/usr/bin/python

# This python scripts extracts the data from the logs that we want to plot and outputs it in a format that gnuplot can
# later on represent.

# Theoretical plot number of combinations
#!/usr/bin/python
import math

if __name__ == '__main__':

########################################################################################################################

    # Mean global flow completion time vs. utilization pFabric
    lambdas = [3600, 5200, 7000, 8900, 11100, 14150, 19000]

    FCTs = [[0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]]
    row = 0

    for x in lambdas:
        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TOY/analysis/flow_completion.statistics"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "less_100KB_99th_fct_ms" in line:
                FCTs[row][0]=line.split("=")[1].split("\n")[0]
                break
        r.close()
        row = row + 1

    w = open('projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/pFabric_less_100KB_99th_fct_ms.dat', 'w')
    w.write("#    TOY\n")
    w.write("3600   %s    \n" % (FCTs[0][0]))
    w.write("5200   %s    \n" % (FCTs[1][0]))
    w.write("7000   %s    \n" % (FCTs[2][0]))
    w.write("8900   %s    \n" % (FCTs[3][0]))
    w.write("11100   %s    \n" % (FCTs[4][0]))
    w.write("14150   %s    \n" % (FCTs[5][0]))
    w.write("19000   %s    \n" % (FCTs[6][0]))
    w.close()


########################################################################################################################

    # Mean global flow completion time vs. utilization pFabric
    lambdas = [3600, 5200, 7000, 8900, 11100, 14150, 19000]

    FCTs = [[0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]]
    row = 0

    for x in lambdas:
        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TOY/analysis/flow_completion.statistics"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "less_100KB_mean_fct_ms" in line:
                FCTs[row][0]=line.split("=")[1].split("\n")[0]
                break
        r.close()
        row = row + 1

    w = open('projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/pFabric_less_100KB_mean_fct_ms.dat', 'w')
    w.write("#	  TOY\n")
    w.write("3600   %s    \n" % (FCTs[0][0]))
    w.write("5200   %s    \n" % (FCTs[1][0]))
    w.write("7000   %s    \n" % (FCTs[2][0]))
    w.write("8900   %s    \n" % (FCTs[3][0]))
    w.write("11100   %s    \n" % (FCTs[4][0]))
    w.write("14150   %s    \n" % (FCTs[5][0]))
    w.write("19000   %s    \n" % (FCTs[6][0]))
    w.close()

########################################################################################################################

    # Mean global flow completion time vs. utilization pFabric
    lambdas = [3600, 5200, 7000, 8900, 11100, 14150, 19000]

    FCTs = [[0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]]
    row = 0

    for x in lambdas:

        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TOY/analysis/flow_completion.statistics"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "geq_1MB_mean_fct_ms" in line:
                FCTs[row][0]=line.split("=")[1].split("\n")[0]
                break
        r.close()
        row = row + 1

    w = open('projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/pFabric_geq_1MB_mean_fct_ms.dat', 'w')
    w.write("#    TOY\n")
    w.write("3600   %s    \n" % (FCTs[0][0]))
    w.write("5200   %s    \n" % (FCTs[1][0]))
    w.write("7000   %s    \n" % (FCTs[2][0]))
    w.write("8900   %s    \n" % (FCTs[3][0]))
    w.write("11100   %s    \n" % (FCTs[4][0]))
    w.write("14150   %s    \n" % (FCTs[5][0]))
    w.write("19000   %s    \n" % (FCTs[6][0]))
    w.close()
