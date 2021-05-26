#include <tofino/constants.p4>
#if __TARGET_TOFINO__ == 2
#include <tofino/intrinsic_metadata.p4>
#else
#include <tofino/intrinsic_metadata.p4>
#endif
#include <tofino/primitives.p4>
#include <tofino/stateful_alu_blackbox.p4>

#include "includes/simpleswitch_defines.p4"
#include "includes/simpleswitch_headers.p4"
#include "includes/simpleswitch_parser.p4"
#include "simpleswitch_routing.p4"
#include "simpleswitch_blackboxs.p4"
#include "simpleswitch_actions.p4"
#include "simpleswitch_tables.p4"

// #include "estimate.p4"
// #### metas

header_type meta_t {
    fields {
        randv: 4;
    }
}
metadata meta_t meta;

action get_random_num_act() {
    modify_field_rng_uniform(meta.randv, 0, 15);
}

table get_random_num_table {
    actions {get_random_num_act;}
    default_action: get_random_num_act;
}

control ingress {
    apply(ipv4_route);
}

control egress {

}