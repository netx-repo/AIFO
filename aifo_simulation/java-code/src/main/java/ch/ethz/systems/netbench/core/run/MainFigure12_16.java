package ch.ethz.systems.netbench.core.run;

import ch.ethz.systems.netbench.core.SelfDefinedFlows;

public class MainFigure12_16 {
    /*
     * Figure 12: Packet distribution logged at the receiver. Three senders send one flow each to a receiver at the same time.
     * The size of the three flows are 100MB (large), 50MB (medium) and 10MB (small), respectively.
     * The link between the switch and the receiver is the bottleneck.
     *
     * Figure 16: The first 300 packets of the small flow logged at the receiver. The setting is the same as Figure 12:
     * Three senders send one flow each to a receiver at the same time. The size of the three flows are 100MB (large),
     * 50MB (medium) and 10MB (small), respectively.
     *
     * The result plots are in projects/aifo/plots/aifo_evaluation/selfDefinedFlows
     */
    public static void main(String args[]) {
        SelfDefinedFlows.setIsSDFTrue();
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/PIFO.properties", "second_transport_layer=udp", "link_bandwidth_bit_per_ns=1", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/SPPIFO.properties", "second_transport_layer=udp", "link_bandwidth_bit_per_ns=1", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/AIFO.properties"
                , "second_transport_layer=udp", "window_size=20", "sample_count=15", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=1", "enable_inversions_tracking=false", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/TCP.properties", "second_transport_layer=udp", "link_bandwidth_bit_per_ns=1", "enable_inversions_tracking=false", "transport_layer=pfabric"});
        SelfDefinedFlows.setIsSDFFalse();

        MainFromProperties.runCommand("python plot_received.py", true); //figure plots
    }
}
