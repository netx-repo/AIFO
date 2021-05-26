package ch.ethz.systems.netbench.core.run;

public class MainFigure8 {
    /*
     * Figure 8: The effect of parameter k
     * Note that despite the property files, all out_port_max_size_packets (C/q_len) are set to 20
     * Result data are stored in java-code/project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_C_K.
     */
    public static void main(String args[]) {

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/3600/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/5200/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/7000/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/8900/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/11100/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/14150/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/19000/AIFO_C30.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.1", "k_value=0.1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/3600/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/5200/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/7000/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/8900/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/11100/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/14150/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/19000/AIFO_C40.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.3", "k_value=0.3"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/5200/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/7000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/8900/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/11100/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/14150/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/19000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/3600/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.9", "k_value=0.9"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/3600/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/5200/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/7000/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/11100/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/14150/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/19000/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_C_K/8900/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=15", "run_folder_name=AIFO_C20_K0.7", "k_value=0.7"});

        MainFromProperties.runCommand("python3 projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_C_K/analyze.py", true);
    }

}
