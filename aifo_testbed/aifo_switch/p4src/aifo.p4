#include <tofino/constants.p4>
#if __TARGET_TOFINO__ == 2
#include <tofino/intrinsic_metadata.p4>
#else
#include <tofino/intrinsic_metadata.p4>
#endif
#include <tofino/primitives.p4>
#include <tofino/stateful_alu_blackbox.p4>

#include "includes/aifo_defines.p4"
#include "includes/aifo_headers.p4"
#include "includes/aifo_parser.p4"
#include "aifo_routing.p4"
#include "aifo_blackboxs.p4"
#include "aifo_actions.p4"
#include "aifo_win.p4"
#include "aifo_tables.p4"

// #include "estimate.p4"
// #### metas
header_type meta_t {
    fields {
        ucast_egress_port: 32;
        qid: 32;

        // rank: 16;
        order: 16;
        tail: 16;
        // qid: 5;
        // queue_length: 19;
        queue_length: 16;
        min_value: 16;

        count_0_0_let: 1;
        count_0_1_let: 1;
        count_0_2_let: 1;
        count_0_3_let: 1;
        count_1_0_let: 1;
        count_1_1_let: 1;
        count_1_2_let: 1;
        count_1_3_let: 1;
        count_2_0_let: 1;
        count_2_1_let: 1;
        count_2_2_let: 1;
        count_2_3_let: 1;
        count_3_0_let: 1;
        count_3_1_let: 1;
        count_3_2_let: 1;
        count_3_3_let: 1;
        count_4_0_let: 1;
        count_4_1_let: 1;
        count_4_2_let: 1;
        count_4_3_let: 1;

        count_0_let: 2;
        count_1_let: 2;
        count_2_let: 2;
        count_3_let: 2;
        count_4_let: 2;

        count_01: 4;
        count_23: 4;

        count_all: 16;

        rank: 32;
    }
}
metadata meta_t meta;


// #### registers
register per_flow_rate_reg {
    width: 64;
    instance_count: NUM_FLOWS;
}

register ig_queue_length_reg {
    width: 64;
    instance_count: NUM_QUEUES;
}

register eg_queue_length_reg {
    width: 64;
    instance_count: NUM_QUEUES;
}

register tail_reg {
    width: 32;
    instance_count: 1;
}


control get_quantile {
    // get quantile and update the window
    // stage x
    apply(check_win_0_0_table);
    apply(check_win_0_1_table);
    apply(check_win_0_2_table);
    apply(check_win_0_3_table);


    // stage x+1
    apply(check_win_1_0_table);
    apply(check_win_1_1_table);
    apply(check_win_1_2_table);
    apply(check_win_1_3_table);


    // stage x+2
    apply(check_win_2_0_table);
    apply(check_win_2_1_table);
    apply(check_win_2_2_table);
    apply(check_win_2_3_table);
    apply(sum_1_0_table);
    apply(sum_1_1_table);
    apply(sum_1_2_table);
    apply(sum_1_3_table);

    // stage x+3
    apply(check_win_3_0_table);
    apply(check_win_3_1_table);
    apply(check_win_3_2_table);
    apply(check_win_3_3_table);
    apply(sum_2_0_table);
    apply(sum_2_1_table);
    apply(sum_2_2_table);
    apply(sum_2_3_table);

    // stage x+4
    apply(check_win_4_0_table);
    apply(check_win_4_1_table);
    apply(check_win_4_2_table);
    apply(check_win_4_3_table);
    apply(sum_3_0_table);
    apply(sum_3_1_table);
    apply(sum_3_2_table);
    apply(sum_3_3_table);

    apply(sum_0_1_2_3_table);

    // get the rank
    apply(sum_all_table);

    // get the rank times 2^10 / 2^11, i.e., (1-K)*C*quantile
    apply(count_mul_table);
}


control get_ig_queue_length {
    // ** get the queue length info from the register (normal packets)
    apply(get_ig_queue_length_table);
}

control routing {
    apply(ipv4_route);
}

control set_ig_queue_length {
    // ** put the queue length info into ingress pipe (worker packets)
    apply(set_ig_queue_length_table);
}

control get_eg_queue_length {
    // ** read the queue length info from egress pipe (worker packets)
    apply(get_eg_queue_length_table);
}

control set_eg_queue_length {
    // ** set the queue length info into the egress pipe (normal packets)
    apply(set_eg_queue_length_table);
}

control bee_recirculate {
    apply(get_qid_table);
    apply(recirculate_table);
}

table get_info_udp_table {
    actions {
        get_info_udp_action;
    }
    default_action: get_info_udp_action;
}

action get_info_udp_action() {
    modify_field(meta.rank, aifo_hdr.rank);
}

table get_info_tcp_table {
    reads {
        ipv4.srcAddr : exact;
        tcp.dstPort  : exact;
    }
    actions {
        get_info_tcp_action;
    }
}

action get_info_tcp_action(rank) {
    modify_field(meta.rank, rank);
}

table subtract_table {
    actions {
        subtract_action;
    }
    default_action: subtract_action;
}
action subtract_action() {
    subtract(meta.queue_length, 25000, meta.queue_length);
}

table get_back_table {
    actions {
        get_back_action;
    }
    default_action: get_back_action;
}

action get_back_action() {
    modify_field(bee_hdr.ucast_egress_port, meta.ucast_egress_port);
    modify_field(bee_hdr.qid, meta.qid);
}

control ingress {
    // Do routing first to get the egress_port and qid info
    routing();

    // Get the rank info
    if (valid(aifo_hdr)) {
        apply(get_info_udp_table);
    }
    else if (valid(tcp)) {
        apply(get_info_tcp_table);
    }

    
    if (valid(bee_hdr)) {
        // The working bee packets are used to maintain the queue length info in 
        // ingress pipe
        apply(get_info_table);
        set_ig_queue_length();
        bee_recirculate();
    }
    else if (valid(udp) or valid(tcp)) {
        // We transform the inequition into (1-K)*C*quantile<=C-c
        // Get queue length c
        get_ig_queue_length();
        // Get C-c
        apply(subtract_table);

        // Get quantile (rank among the items in the window)
        apply(get_tail_table);
        get_quantile();

        // ** make some decision here 
        apply(get_min_table);
        if (meta.min_value == meta.queue_length) {
            apply(drop_table);
        }
    }
}

control egress {
    if (valid(bee_hdr)) {
        get_eg_queue_length();
        apply(get_back_table);
    }
    else {
        set_eg_queue_length();
    }
}