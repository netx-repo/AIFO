#define AIFO_PORT         9000
#define BEE_PORT          9999
#define NUM_QUEUES        500
#define NUM_FLOWS         500
#define SAMPLE_COUNT      1

#define TABLE_CHECK_WINDOW(i,j) \
    table check_win_##i##_##j##_table { \
        actions { \
            check_win_##i##_##j##_action; \
        } \
        default_action: check_win_##i##_##j##_action; \
    }

#define ACTION_CHECK_WINDOW(i,j) \
    action check_win_##i##_##j##_action() { \
        check_win_##i##_##j##_alu.execute_stateful_alu(0); \
    }

#define BLACKBOX_CHECK_WINDOW(i,j) \
    blackbox stateful_alu check_win_##i##_##j##_alu { \
        reg: window_##i##_##j##_register; \
\
        condition_lo: meta.rank < register_lo; \
        condition_hi: meta.tail == (i*4 + j) * SAMPLE_COUNT; \
\
        update_lo_1_predicate: condition_hi; \
        update_lo_1_value:     meta.rank; \
\
        update_hi_1_predicate: condition_lo; \
        update_hi_1_value:     1; \
        update_hi_2_predicate: not condition_lo; \
        update_hi_2_value:     0; \
\
        output_value:          alu_hi; \
        output_dst:            meta.count_##i##_##j##_let; \
   }

#define BLACKBOX_CHECK_WINDOW_34(i,j,k) \
    blackbox stateful_alu check_win_##i##_##j##_alu { \
        reg: window_##i##_##j##_register; \
\
        condition_lo: meta.rank < register_lo; \
        condition_hi: meta.tail == (i*4 + j) * SAMPLE_COUNT; \
\
        update_lo_1_predicate: condition_hi; \
        update_lo_1_value:     meta.rank; \
\
        update_hi_1_predicate: condition_lo; \
        update_hi_1_value:     1; \
        update_hi_2_predicate: not condition_lo; \
        update_hi_2_value:     0; \
\
        output_value:          alu_hi; \
        output_dst:            meta.count_##k##_##j##_let; \
}

#define TABLE_SUM(i,j) \
    table sum_##i##_##j##_table { \
        actions { \
            sum_##i##_##j##_action; \
        } \
        default_action: sum_##i##_##j##_action; \
    }

#define ACTION_SUM(i,j) \
    action sum_##i##_##j##_action() { \
        add(meta.count_0_##j##_let, meta.count_0_##j##_let, meta.count_##i##_##j##_let); \
    }

#define REG_WIN(i,j) \
    register window_##i##_##j##_register { \
        width:64; \
        instance_count: 1; \
    }