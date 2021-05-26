// ** worker packets
action set_ig_queue_length_action(index) {
    set_ig_queue_length_alu.execute_stateful_alu(index);
}

action get_qid_action() {
    modify_field(bee_hdr.ucast_egress_port, ig_intr_md_for_tm.ucast_egress_port);
    modify_field(bee_hdr.qid, ig_intr_md_for_tm.qid);
}

action get_eg_queue_length_action(index) {
    get_eg_queue_length_alu.execute_stateful_alu(index);
}

action recirculate_action() {
    recirculate(68);
}

// ** aifo packets
action get_info_action() {
    modify_field(meta.ucast_egress_port, bee_hdr.ucast_egress_port);
    modify_field(meta.qid, bee_hdr.qid);
    modify_field(meta.queue_length, bee_hdr.queue_length);
}

action get_ig_queue_length_action(index) {
    get_ig_queue_length_alu.execute_stateful_alu(index);
}

action set_eg_queue_length_action(index) {
    set_eg_queue_length_alu.execute_stateful_alu(index);
}

action sum_0_1_2_3_action() {
    add(meta.count_0_0_let, meta.count_0_0_let, meta.count_0_1_let);
    add(meta.count_0_2_let, meta.count_0_2_let, meta.count_0_3_let);
}

action sum_all_action() {
    add(meta.count_all, meta.count_0_0_let, meta.count_0_2_let);
}

action count_mul_action() {
    shift_left(meta.count_all, meta.count_all, 10);
}

action get_tail_action() {
    get_tail_alu.execute_stateful_alu(0);
}

action get_min_action() {
    min(meta.min_value, meta.count_all, meta.queue_length);
}

action get_sum_action() {
    add(meta.count_all, meta.count_all, meta.queue_length);
}