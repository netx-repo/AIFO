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

    Inversions = [[0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0]]
    row = 0

    for x in lambdas:
        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/SPPIFO/inversions_tracking.csv.log"
        r = open(file, 'r')
        count_server = 0
        for i, line in enumerate(r):
            #<144, filter out
            id = line.split(',')[0]
            if int(id) < 144:
                count_server += 1
        Inversions[row][0] = i+1 - count_server
        r.close()

        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TOY/inversions_tracking.csv.log"
        r = open(file, 'r')
        for i, line in enumerate(r):
            pass
        Inversions[row][1] = i+1
        r.close()
        row = row + 1

    w = open('projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/number_of_inversions.dat', 'w')
    w.write("#    SPPIFO    TOY\n")
    w.write("3600   %s    %s    \n" % (Inversions[0][0], Inversions[0][1]))
    w.write("5200   %s    %s    \n" % (Inversions[1][0], Inversions[1][1]))
    w.write("7000   %s    %s    \n" % (Inversions[2][0], Inversions[2][1]))
    w.write("8900   %s    %s    \n" % (Inversions[3][0], Inversions[3][1]))
    w.write("11100   %s    %s    \n" % (Inversions[4][0], Inversions[4][1]))
    w.write("14150   %s    %s    \n" % (Inversions[5][0], Inversions[5][1]))
    w.write("19000   %s    %s    \n" % (Inversions[6][0], Inversions[6][1]))
    w.close()


########################################################################################################################

    # Mean global flow completion time vs. utilization pFabric
    lambdas = [3600, 5200, 7000, 8900, 11100, 14150, 19000]

    Inversions = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]
    row = 0

    for x in lambdas:
        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TCP/statistics.log"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "PACKETS_DROPPED" in line:
                Inversions[row][0]=line.split(":")[1].split()[0].split("\n")[0]
                break
        r.close()

        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/PIFO/statistics.log"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "PACKETS_DROPPED" in line:
                Inversions[row][1]=line.split(":")[1].split()[0].split("\n")[0]
                break
        r.close()

        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/SPPIFO/statistics.log"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "PACKETS_DROPPED" in line:
                Inversions[row][2]=line.split(":")[1].split()[0].split("\n")[0]
                break
        r.close()

        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TOY/statistics.log"
        r = open(file, 'r')
        lines = r.readlines()
        for i, line in enumerate(lines):
            if "PACKETS_DROPPED" in line:
                Inversions[row][3]=line.split(":")[1].split()[0].split("\n")[0]
                break
        r.close()
        row = row + 1

    w = open('projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/packets_dropped.dat', 'w')
    w.write("#    TCP    PIFO    SPPIFO    TOY\n")
    w.write("3600   %s    %s    %s    %s    \n" % (Inversions[0][0], Inversions[0][1], Inversions[0][2], Inversions[0][3]))
    w.write("5200   %s    %s    %s    %s    \n" % (Inversions[1][0], Inversions[1][1], Inversions[1][2], Inversions[1][3]))
    w.write("7000   %s    %s    %s    %s    \n" % (Inversions[2][0], Inversions[2][1], Inversions[2][2], Inversions[2][3]))
    w.write("8900   %s    %s    %s    %s    \n" % (Inversions[3][0], Inversions[3][1], Inversions[3][2], Inversions[3][3]))
    w.write("11100   %s    %s    %s    %s    \n" % (Inversions[4][0], Inversions[4][1], Inversions[4][2], Inversions[4][3]))
    w.write("14150   %s    %s    %s    %s    \n" % (Inversions[5][0], Inversions[5][1], Inversions[5][2], Inversions[5][3]))
    w.write("19000   %s    %s    %s    %s    \n" % (Inversions[6][0], Inversions[6][1], Inversions[6][2], Inversions[6][3]))
    w.close()