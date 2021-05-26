package ch.ethz.systems.netbench.core.run;

public class MainFigure11 {
    /*
     * Figure 11: The effect of queue length on 10G/40G network.
     * Result data are stored in java-code/project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len
     */

    public static void main(String args[]) {
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=10", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=50", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C100.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=100", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C200.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=200", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C500.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=500", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/3600/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/5200/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/7000/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/8900/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/11100/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/19000/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len/14150/AIFO_C1000.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=1000", "link_bandwidth_bit_per_ns=10", "sample_count=15", "k_value=0.1"});

        /* Analyze */
        MainFromProperties.runCommand("python3 projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len/analyze.py", true);

    }
}
