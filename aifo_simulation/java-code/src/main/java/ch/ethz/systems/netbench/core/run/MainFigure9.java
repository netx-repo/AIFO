package ch.ethz.systems.netbench.core.run;

import ch.ethz.systems.netbench.core.run.MainFromProperties;

public class MainFigure9 {
    /*
     * Figure 9: The effect of window length and sampling rate
     * Result data are stored in java-code/project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_w_sr.
     */
    public static void main(String args[]) {
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/3600/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/5200/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/7000/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/8900/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/11100/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/14150/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/19000/AIFO_C10.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W20_SR1"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/3600/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/5200/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/7000/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/8900/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/11100/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/14150/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/19000/AIFO_C20.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=50", "k_value=0.1", "run_folder_name=AIFO_W20_SR0.02"});


        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/3600/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/5200/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/7000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/8900/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/11100/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/14150/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/19000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=1000", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=1", "k_value=0.1", "run_folder_name=AIFO_W1000_SR1"});


        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/3600/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/5200/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/7000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/8900/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/11100/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/14150/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_sample_rate/19000/AIFO_C50.properties"
                , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=100", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "sample_count=10", "k_value=0.1", "run_folder_name=AIFO_W100_SR0.1"});


        /* Analyze and plot */
        MainFromProperties.runCommand("python3 projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload_w_sr/analyze.py", true);
    }
}
