load 'projects/sppifo/plots/spectral.pal'

set terminal pdfcairo
set term pdfcairo enhanced font "Helvetica,16" size 4in,2.5in

########################################################################################################################
# Mean flow completion time: pFabric-based scheduling schemes
########################################################################################################################
set output 'projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload_C_K/pFabric_less_100KB_99th_fct_ms.pdf'

set xlabel 'Load'
set xrange [0:6]
set xtics ("0.2" 0, "0.3" 1, "0.4" 2, "0.5" 3, "0.6" 4, "0.7" 5, "0.8" 6)

set ylabel 'Flow Completion Time (ms)'
set yrange [0:9]
set key outside
plot "projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload_C_K/pFabric_less_100KB_99th_fct_ms.dat" using 2 title "C20 K0" w lp  ls 21 lw 4, \
            '' using 3 title "C20 K0.1"  w lp ls 23 lw 4, \
            '' using 4 title "C20 K0.3" w lp ls 27 lw 4, \
            '' using 5 title "C20 K0.5" w lp ls 11 lw 4, \
            '' using 6 title "C20 K0.7" w lp ls 30 lw 4, \
            '' using 7 title "C20 K0.9" w lp ls 35 lw 4


########################################################################################################################
# Mean flow completion time <100KB: pFabric-based scheduling schemes
########################################################################################################################
set output 'projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload_C_K/pFabric_less_100KB_mean_fct_ms.pdf'

set xlabel 'Load'
set ylabel 'Flow Completion Time (ms)'
set yrange [0:2.5]
set ytics 2
set key outside
plot "projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload_C_K/pFabric_less_100KB_mean_fct_ms.dat" using 2 title "C20 K0" w lp  ls 21 lw 4, \
            '' using 3 title "C20 K0.1"  w lp ls 23 lw 4, \
            '' using 4 title "C20 K0.3" w lp ls 27 lw 4, \
            '' using 5 title "C20 K0.5" w lp ls 11 lw 4, \
            '' using 6 title "C20 K0.7" w lp ls 30 lw 4, \
            '' using 7 title "C20 K0.9" w lp ls 35 lw 4

########################################################################################################################
# Mean flow completion time >10MB: pFabric-based scheduling schemes
########################################################################################################################
set output 'projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload_C_K/pFabric_geq_1MB_mean_fct_ms.pdf'

set xlabel 'Load'
set ylabel 'Flow Completion Time (ms)'
set yrange [0:100]
set ytics auto
set key outside
plot "projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload_C_K/pFabric_geq_1MB_mean_fct_ms.dat" using 2 title "C20 K0" w lp  ls 21 lw 4, \
            '' using 3 title "C20 K0.1"  w lp ls 23 lw 4, \
            '' using 4 title "C20 K0.3" w lp ls 27 lw 4, \
            '' using 5 title "C20 K0.5" w lp ls 11 lw 4, \
            '' using 6 title "C20 K0.7" w lp ls 30 lw 4, \
            '' using 7 title "C20 K0.9" w lp ls 35 lw 4
