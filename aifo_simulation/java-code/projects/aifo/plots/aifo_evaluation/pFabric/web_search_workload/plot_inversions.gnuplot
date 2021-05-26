load 'projects/sppifo/plots/spectral.pal'

set terminal pdfcairo
set term pdfcairo enhanced font "Helvetica,16" size 4in,2.5in

########################################################################################################################
# Mean flow completion time: pFabric-based scheduling schemes
########################################################################################################################
set output 'projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/packets_dropped.pdf'

set xlabel 'Load'
set xrange [0:6]
set xtics ("0.2" 0, "0.3" 1, "0.4" 2, "0.5" 3, "0.6" 4, "0.7" 5, "0.8" 6)

set ylabel 'Packets Dropped'
set yrange [0:774112]
set key outside
plot "projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/packets_dropped.dat" using 2 title "TCP" w lp  ls 21 lw 4, \
            '' using 3 title "PIFO"  w lp ls 23 lw 4, \
            '' using 4 title "SPPIFO" w lp ls 27 lw 4, \
            '' using 5 title "TOY"  w lp ls 28 lw 4


########################################################################################################################
# Mean flow completion time <100KB: pFabric-based scheduling schemes
########################################################################################################################
set output 'projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/number_of_inversions.pdf'

set xlabel 'Load'
set ylabel 'Number of Inversions'
set yrange [0:28535445]
set ytics 2
set key outside
plot "projects/sppifo/plots/sppifo_evaluation/pFabric/web_search_workload/number_of_inversions.dat" using 2 title "SPPIFO" w lp  ls 21 lw 4, \
            '' using 3 title "TOY"  w lp ls 23 lw 4
