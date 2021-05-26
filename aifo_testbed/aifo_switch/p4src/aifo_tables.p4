// ** worker packets
@pragma stage 1
table set_ig_queue_length_table {
    reads {
        bee_hdr.ucast_egress_port: exact;
        bee_hdr.qid: exact;
    }
    actions {
        set_ig_queue_length_action;
    }
    default_action: set_ig_queue_length_action;
}

table get_qid_table {
    actions {
        get_qid_action;
    }
    default_action: get_qid_action;
}

table get_eg_queue_length_table {
    reads {
        meta.ucast_egress_port: exact;
        meta.qid: exact;
    }
    actions {
        get_eg_queue_length_action;
    }
    default_action: get_eg_queue_length_action;
}

table recirculate_table {
    actions {
        recirculate_action;
    }
    default_action: recirculate_action;
}


// ** aifo packets
table get_info_table {
    actions {
        get_info_action;
    }
    default_action: get_info_action;
}

table get_ig_queue_length_table {
    reads {
        ig_intr_md_for_tm.ucast_egress_port: exact;
        ig_intr_md_for_tm.qid: exact;
    }
    actions {
        get_ig_queue_length_action;
    }
    default_action: get_ig_queue_length_action;
}

table set_eg_queue_length_table {
    reads {
        ig_intr_md_for_tm.ucast_egress_port: exact;
        ig_intr_md_for_tm.qid: exact;
    }
    actions {
        set_eg_queue_length_action;
    }
    default_action: set_eg_queue_length_action;
}

table sum_0_1_2_3_table {
    actions {
        sum_0_1_2_3_action;
    }
    default_action: sum_0_1_2_3_action;
}

table sum_all_table {
    actions {
        sum_all_action;
    }
    default_action: sum_all_action;
}

table count_mul_table {
    actions {
        count_mul_action;
    }
    default_action: count_mul_action;
}

table get_tail_table {
    actions {
        get_tail_action;
    }
    default_action: get_tail_action;
}

table get_min_table {
    actions {
        get_min_action;
    }
    default_action: get_min_action;
}

table get_sum_table {
    actions {
        get_sum_action;
    }
    default_action: get_sum_action;
}

table drop_table {
    actions {
        _drop;
    }
    default_action: _drop;
}