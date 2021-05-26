#!/usr/bin/python

# This python scripts extracts the data from the logs that we want to plot and outputs it in a format that gnuplot can
# later on represent.

# Theoretical plot number of combinations
#!/usr/bin/python
import math

if __name__ == '__main__':

########################################################################################################################

    # Mean global flow completion time vs. utilization pFabric
    lambdas = [3600, 5200, 7000, 8900, 11100]

    Inversions = [[0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0]]
    row = 0

    for x in lambdas:
        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/SPPIFO/inversions_tracking.csv.log"
        r = open(file, 'r')
        count_inversion = 0
        for i, line in enumerate(r):
            #<144, filter out
            id = line.split(',')[0]
            if int(id) >= 144:
                count_inversion += int(line.split(',')[2])
        Inversions[row][0] = count_inversion
        r.close()

        file = "temp/sppifo/sppifo_evaluation/pFabric/web_search_workload/"+str(x)+"/TOY/inversions_tracking.csv.log"
        r = open(file, 'r')
        count_inversion = 0
        for i, line in enumerate(r):
            count_inversion += int(line.split(',')[2])
        Inversions[row][1] = count_inversion
        r.close()
        row = row + 1

    w = open('projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/number_of_inversions.dat', 'w')
    w.write("#    SPPIFO    TOY\n")
    w.write("3600   %s    %s    \n" % (Inversions[0][0], Inversions[0][1]))
    w.write("5200   %s    %s    \n" % (Inversions[1][0], Inversions[1][1]))
    w.write("7000   %s    %s    \n" % (Inversions[2][0], Inversions[2][1]))
    w.write("8900   %s    %s    \n" % (Inversions[3][0], Inversions[3][1]))
    w.write("11100   %s    %s    \n" % (Inversions[4][0], Inversions[4][1]))
    w.close()