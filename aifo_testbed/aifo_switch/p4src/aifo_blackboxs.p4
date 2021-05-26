// ** worker packets
blackbox stateful_alu set_ig_queue_length_alu {
    reg: ig_queue_length_reg;

    condition_hi: register_hi >= 100;

    update_hi_1_predicate: condition_hi;
    update_hi_1_value: 1;
    update_hi_2_predicate: not condition_hi;
    update_hi_2_value: register_hi + 1;
    

    update_lo_1_value:  bee_hdr.queue_length;
}

blackbox stateful_alu get_eg_queue_length_alu {
    reg: eg_queue_length_reg;

    condition_hi: register_hi >= 100;

    update_hi_1_predicate: condition_hi;
    update_hi_1_value: 1;
    update_hi_2_predicate: not condition_hi;
    update_hi_2_value: register_hi + 2;

    output_value:           register_lo;
    output_dst:             bee_hdr.queue_length;
}

// ** aifo packets
blackbox stateful_alu get_ig_queue_length_alu {
    reg: ig_queue_length_reg;

    condition_hi: register_hi >= 100;

    update_hi_1_predicate: condition_hi;
    update_hi_1_value: 1;
    update_hi_2_predicate: not condition_hi;
    update_hi_2_value: register_hi + 2;
    
    output_value:           register_lo;
    output_dst:             meta.queue_length;
}

blackbox stateful_alu set_eg_queue_length_alu {
    reg: eg_queue_length_reg;

    condition_hi: register_hi >= 100;

    update_lo_1_value:      eg_intr_md.deq_qdepth;

    update_hi_1_predicate: condition_hi;
    update_hi_1_value: 1;
    update_hi_2_predicate: not condition_hi;
    update_hi_2_value: register_hi + 1;
}

blackbox stateful_alu get_tail_alu {
    reg: tail_reg;

    condition_lo: register_lo < 16 * SAMPLE_COUNT - 1;

    update_lo_1_predicate: condition_lo;
    update_lo_1_value:     register_lo + 1;
    update_lo_2_predicate: not condition_lo;
    update_lo_2_value:     0;

    output_value:          register_lo;
    output_dst:            meta.tail;
}