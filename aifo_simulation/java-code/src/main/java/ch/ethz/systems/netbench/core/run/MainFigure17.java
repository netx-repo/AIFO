package ch.ethz.systems.netbench.core.run;

public class MainFigure17 {
    public static void main(String args[]) {
        System.out.println("Creating data for Figure 17");

        int loads[] = {89000, 111000, 141500, 190000};
        double k_values[] = {0.1, 0.3, 0.7, 0.9};
        int q_lens[] = {100, 250, 375, 500};

        int start_trial = 12; //first trial is 1


        int trial_count= 0;
        for (int i = 0; i < loads.length; i++) {
            for (int j = 0; j < k_values.length; j++) {
                for (int k = 0; k < q_lens.length; k++) {
                    String folderName = String.format("AIFO_L%d_C%d_K%d", loads[i], q_lens[k], (long)(k_values[j]*100));

                    String arg1 = String.format("traffic_lambda_flow_starts_per_s=%d", loads[i]);
                    String arg2 = String.format("k_value=%,.2f", k_values[j]);
                    String arg3 = String.format("output_port_max_size_packets=%d", q_lens[k]);
                    String arg4 = String.format("run_folder_name=%s", folderName);

                    trial_count++;
                    if(trial_count < start_trial){
                        System.out.println(String.format("Skipping trial #%d: %s", trial_count, folderName));
                    } else {
                        System.out.println(String.format("Running trial #%d: %s", trial_count, folderName));

                        boolean trial_succeeded = false;
                        int trial_attempts_remaining = 5;

                        while(!trial_succeeded){
                            try {
                                trial_attempts_remaining--;
                                MainFromProperties.main(new String[]{"projects/aifo/runs/aifo_evaluation/pFabric/web_search_workload_q_len_and_K/AIFO_DEFAULT.properties", "second_transport_layer=udp", arg1, "window_size=20", arg3, "link_bandwidth_bit_per_ns=10", "sample_count=15", arg2, arg4});
                                trial_succeeded = true;
                            } catch (Exception e) {
                                System.out.println(e);
                                if(trial_attempts_remaining >= 0){
                                    System.out.println(String.format("Trying again\nTrial attempts remaining: %d", trial_attempts_remaining));
                                } else {
                                    System.out.println("Failed too much, exiting...");
                                    System.exit(1);
                                }
                            }
                        }
                    }

                }
            }
        }

    }
}
