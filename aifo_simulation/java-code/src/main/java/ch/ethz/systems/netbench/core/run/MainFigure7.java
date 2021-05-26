package ch.ethz.systems.netbench.core.run;

public class MainFigure7 {
    /*
     * Figure 7 Simulation results of web search workload to minimize FCT.
     * Result data are stored in java-code/project/aifo/plots/aifo_evaluation/pFabric/web_search_workload.
     * Since we are doing 10G/40G, overwrite traffice_lambda_flow_starts_per_s and link_bandwidth_bit_per_ns
     * to original_lambda*10 and 10 respectively.
     */

    public static void main(String args[]) {

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/AIFO.properties"
        , "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "window_size=20", "sample_count=15", "output_port_max_size_packets=20", "link_bandwidth_bit_per_ns=10", "k_value=0.1"});


        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/3600/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=36000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/5200/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=52000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/7000/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=70000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/8900/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=89000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/11100/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=111000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/14150/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=141500", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/DCTCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/TCP.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/PIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});
        MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload/19000/SPPIFO.properties", "second_transport_layer=udp", "traffic_lambda_flow_starts_per_s=190000", "link_bandwidth_bit_per_ns=10", "enable_inversions_tracking=false"});

        /* Analyze and plot */
        MainFromProperties.runCommand("python3 projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload/analyze.py", true);
    }
}
