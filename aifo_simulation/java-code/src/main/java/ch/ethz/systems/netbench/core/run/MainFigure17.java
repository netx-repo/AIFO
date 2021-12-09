package ch.ethz.systems.netbench.core.run;

public class MainFigure17 {
    public static void main(String args[]) {
        System.out.println("Creating data for Figure 17");

        int loads[] = {89000, 111000, 141500, 190000};
        double k_values[] = {0.1, 0.3, 0.7, 0.9};
        int q_lens[] = {100, 250, 375, 500};

        for (int load : loads) {
            for (double k_value : k_values) {
                for (int q_len : q_lens) {
                    String folderName = String.format("AIFO_L%d_C%d_K%d", load, q_len, (long)(k_value*100));

                    String arg1 = String.format("traffic_lambda_flow_starts_per_s=%d", load);
                    String arg2 = String.format("k_value=%,.2f", k_value);
                    String arg3 = String.format("output_port_max_size_packets=%d", q_len);
                    String arg4 = String.format("run_folder_name=%s", folderName);

                    MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/AIFO_DEFAULT.properties"
                , "second_transport_layer=udp", arg1, "window_size=20", arg3, "link_bandwidth_bit_per_ns=10", "sample_count=15", arg2, arg4});

                }
            }
        }

    }
}
