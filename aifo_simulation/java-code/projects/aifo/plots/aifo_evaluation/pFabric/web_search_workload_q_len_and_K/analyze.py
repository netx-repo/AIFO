# This python scripts extracts the data from the logs that we want to plot and outputs it in a format that gnuplot can
# later on represent.

import math

if __name__ == '__main__':

    # Mean global flow completion time vs. utilization pFabric
    lambdas = [8900, 11100, 14150, 19000]

    # Queue sizes
    qs = [100, 250, 375, 500]

    # K values
    ks = [10, 30, 70, 90]

    FCTs = [
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    ]

    r = 0
    c = 0
    d = 0

    foldername = "temp/aifo/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/AIFO_L"
    arg1 = "_C"
    arg2 = "_K"
    arg3 = "/analysis/flow_completion.statistics"

    for i in qs:
        for j in lambdas:
            for k in ks:
                arg1 += str(i)
                arg2 += str(k)
                file = foldername + str(j * 10) + arg1 + arg2 + arg3
                print(file)
                arg1 = "_C"
                arg2 = "_K"
                fr = open(file, 'r')
                lines = fr.readlines()
                for l, line, in enumerate(lines):
                    if "less_100KB_mean_fct_ms" in line:
                        FCTs[r][c][d] = line.split("=")[1].split("\n")[0]
                        break
                fr.close()
                d += 1
            c += 1
            d = 0
        r += 1
        c = 0
        d = 0

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_less_100KB_mean_fct_ms_C100.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[0][0][0], FCTs[0][0][1], FCTs[0][0][2], FCTs[0][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[0][1][0], FCTs[0][1][1], FCTs[0][1][2], FCTs[0][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[0][2][0],
    FCTs[0][2][1], FCTs[0][2][2], FCTs[0][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[0][3][0],
    FCTs[0][3][1], FCTs[0][3][2], FCTs[0][3][3]))

    fw.close()

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_less_100KB_mean_fct_ms_C250.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[1][0][0], FCTs[1][0][1], FCTs[1][0][2], FCTs[1][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[1][1][0], FCTs[1][1][1], FCTs[1][1][2], FCTs[1][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[1][2][0],
    FCTs[1][2][1], FCTs[1][2][2], FCTs[1][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[1][3][0],
    FCTs[1][3][1], FCTs[1][3][2], FCTs[1][3][3]))

    fw.close()

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_less_100KB_mean_fct_ms_C375.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[2][0][0], FCTs[2][0][1], FCTs[2][0][2], FCTs[2][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[2][1][0], FCTs[2][1][1], FCTs[2][1][2], FCTs[2][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[2][2][0],
    FCTs[2][2][1], FCTs[2][2][2], FCTs[2][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[2][3][0],
    FCTs[2][3][1], FCTs[2][3][2], FCTs[2][3][3]))

    fw.close()

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_less_100KB_mean_fct_ms_C500.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[3][0][0], FCTs[3][0][1], FCTs[3][0][2], FCTs[3][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[3][1][0], FCTs[3][1][1], FCTs[3][1][2], FCTs[3][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[3][2][0],
    FCTs[3][2][1], FCTs[3][2][2], FCTs[3][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[3][3][0],
    FCTs[3][3][1], FCTs[3][3][2], FCTs[3][3][3]))

    fw.close()

    FCTs = [
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    ]

    r = 0
    c = 0
    d = 0

    for i in qs:
        for j in lambdas:
            for k in ks:
                arg1 += str(i)
                arg2 += str(k)
                file = foldername + str(j * 10) + arg1 + arg2 + arg3
                print(file)
                arg1 = "_C"
                arg2 = "_K"
                fr = open(file, 'r')
                lines = fr.readlines()
                for l, line, in enumerate(lines):
                    if "geq_1MB_mean_fct_ms" in line:
                        FCTs[r][c][d] = line.split("=")[1].split("\n")[0]
                        break
                fr.close()
                d += 1
            c += 1
            d = 0
        r += 1
        c = 0
        d = 0

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_geq_1MB_mean_fct_ms_C100.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[0][0][0], FCTs[0][0][1], FCTs[0][0][2], FCTs[0][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[0][1][0], FCTs[0][1][1], FCTs[0][1][2], FCTs[0][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[0][2][0],
    FCTs[0][2][1], FCTs[0][2][2], FCTs[0][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[0][3][0],
    FCTs[0][3][1], FCTs[0][3][2], FCTs[0][3][3]))

    fw.close()

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_geq_1MB_mean_fct_ms_C250.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[1][0][0], FCTs[1][0][1], FCTs[1][0][2], FCTs[1][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[1][1][0], FCTs[1][1][1], FCTs[1][1][2], FCTs[1][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[1][2][0],
    FCTs[1][2][1], FCTs[1][2][2], FCTs[1][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[1][3][0],
    FCTs[1][3][1], FCTs[1][3][2], FCTs[1][3][3]))

    fw.close()

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_geq_1MB_mean_fct_ms_C375.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[2][0][0], FCTs[2][0][1], FCTs[2][0][2], FCTs[2][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[2][1][0], FCTs[2][1][1], FCTs[2][1][2], FCTs[2][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[2][2][0],
    FCTs[2][2][1], FCTs[2][2][2], FCTs[2][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[2][3][0],
    FCTs[2][3][1], FCTs[2][3][2], FCTs[2][3][3]))

    fw.close()

    fw = open('projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/pFabric_geq_1MB_mean_fct_ms_C500.dat', 'w')

    fw.write("#    K1    K3    K7    K9\n")
    fw.write("89000    %s    %s    %s    %s    \n" % (FCTs[3][0][0], FCTs[3][0][1], FCTs[3][0][2], FCTs[3][0][3]))
    fw.write("111000    %s    %s    %s    %s    \n" % (FCTs[3][1][0], FCTs[3][1][1], FCTs[3][1][2], FCTs[3][1][3]))
    fw.write("141500    %s    %s    %s    %s    \n" % (FCTs[3][2][0],
    FCTs[3][2][1], FCTs[3][2][2], FCTs[3][2][3]))
    fw.write("190000    %s    %s    %s    %s    \n" % (FCTs[3][3][0],
    FCTs[3][3][1], FCTs[3][3][2], FCTs[3][3][3]))
    fw.close()
