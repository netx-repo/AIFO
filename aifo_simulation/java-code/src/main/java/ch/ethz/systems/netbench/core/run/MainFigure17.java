package ch.ethz.systems.netbench.core.run;

public class MainFigure17 {
    public static void main(String args[]) {
        System.out.println("Creating Figure 17");
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/8900/K1/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
    }
}
