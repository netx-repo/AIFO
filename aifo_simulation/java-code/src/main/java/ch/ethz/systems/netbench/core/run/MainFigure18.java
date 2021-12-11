package ch.ethz.systems.netbench.core.run;
import ch.ethz.systems.netbench.core.SelfDefinedFlows;

public class MainFigure18 {
    
    public static void main(String args[]) {

        
        System.out.println("Creating Figure 18");
        
        int q_lens[] = {100, 250, 375, 500};

        SelfDefinedFlows.setIsSDFTrue();

        for (int q_len : q_lens){

            MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len_order/3600/PIFO.properties", String.format("run_folder_name=PIFO_C%d", q_len), "second_transport_layer=udp", "link_bandwidth_bit_per_ns=1", String.format("output_port_max_size_packets=%d", q_len), "enable_inversions_tracking=false"});
            MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len_order/3600/AIFO.properties", String.format("run_folder_name=AIFO_C%d", q_len), "second_transport_layer=udp", "window_size=20", "sample_count=15", String.format("output_port_max_size_packets=%d", q_len), "link_bandwidth_bit_per_ns=1", "enable_inversions_tracking=false", "k_value=0.1"});

        }

        SelfDefinedFlows.setIsSDFFalse();

        MainFromProperties.runCommand("python plot_received_18.py", true); //figure plots
    }
}
