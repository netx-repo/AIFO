TABLE_CHECK_WINDOW(0,0)
TABLE_CHECK_WINDOW(0,1)
TABLE_CHECK_WINDOW(0,2)
TABLE_CHECK_WINDOW(0,3)
TABLE_CHECK_WINDOW(1,0)
TABLE_CHECK_WINDOW(1,1)
TABLE_CHECK_WINDOW(1,2)
TABLE_CHECK_WINDOW(1,3)
TABLE_CHECK_WINDOW(2,0)
TABLE_CHECK_WINDOW(2,1)
TABLE_CHECK_WINDOW(2,2)
TABLE_CHECK_WINDOW(2,3)
TABLE_CHECK_WINDOW(3,0)
TABLE_CHECK_WINDOW(3,1)
TABLE_CHECK_WINDOW(3,2)
TABLE_CHECK_WINDOW(3,3)
TABLE_CHECK_WINDOW(4,0)
TABLE_CHECK_WINDOW(4,1)
TABLE_CHECK_WINDOW(4,2)
TABLE_CHECK_WINDOW(4,3)

ACTION_CHECK_WINDOW(0,0)
ACTION_CHECK_WINDOW(0,1)
ACTION_CHECK_WINDOW(0,2)
ACTION_CHECK_WINDOW(0,3)
ACTION_CHECK_WINDOW(1,0)
ACTION_CHECK_WINDOW(1,1)
ACTION_CHECK_WINDOW(1,2)
ACTION_CHECK_WINDOW(1,3)
ACTION_CHECK_WINDOW(2,0)
ACTION_CHECK_WINDOW(2,1)
ACTION_CHECK_WINDOW(2,2)
ACTION_CHECK_WINDOW(2,3)
ACTION_CHECK_WINDOW(3,0)
ACTION_CHECK_WINDOW(3,1)
ACTION_CHECK_WINDOW(3,2)
ACTION_CHECK_WINDOW(3,3)
ACTION_CHECK_WINDOW(4,0)
ACTION_CHECK_WINDOW(4,1)
ACTION_CHECK_WINDOW(4,2)
ACTION_CHECK_WINDOW(4,3)

BLACKBOX_CHECK_WINDOW(0,0)
BLACKBOX_CHECK_WINDOW(0,1)
BLACKBOX_CHECK_WINDOW(0,2)
BLACKBOX_CHECK_WINDOW(0,3)
BLACKBOX_CHECK_WINDOW(1,0)
BLACKBOX_CHECK_WINDOW(1,1)
BLACKBOX_CHECK_WINDOW(1,2)
BLACKBOX_CHECK_WINDOW(1,3)
BLACKBOX_CHECK_WINDOW(2,0)
BLACKBOX_CHECK_WINDOW(2,1)
BLACKBOX_CHECK_WINDOW(2,2)
BLACKBOX_CHECK_WINDOW(2,3)
// BLACKBOX_CHECK_WINDOW(3,0)
// BLACKBOX_CHECK_WINDOW(3,1)
// BLACKBOX_CHECK_WINDOW(3,2)
// BLACKBOX_CHECK_WINDOW(3,3)
// BLACKBOX_CHECK_WINDOW(4,0)
// BLACKBOX_CHECK_WINDOW(4,1)
// BLACKBOX_CHECK_WINDOW(4,2)
// BLACKBOX_CHECK_WINDOW(4,3)
BLACKBOX_CHECK_WINDOW_34(3,0,1)
BLACKBOX_CHECK_WINDOW_34(3,1,1)
BLACKBOX_CHECK_WINDOW_34(3,2,1)
BLACKBOX_CHECK_WINDOW_34(3,3,1)
BLACKBOX_CHECK_WINDOW_34(4,0,2)
BLACKBOX_CHECK_WINDOW_34(4,1,2)
BLACKBOX_CHECK_WINDOW_34(4,2,2)
BLACKBOX_CHECK_WINDOW_34(4,3,2)

TABLE_SUM(0,0)
TABLE_SUM(0,1)
TABLE_SUM(0,2)
TABLE_SUM(0,3)
TABLE_SUM(1,0)
TABLE_SUM(1,1)
TABLE_SUM(1,2)
TABLE_SUM(1,3)
TABLE_SUM(2,0)
TABLE_SUM(2,1)
TABLE_SUM(2,2)
TABLE_SUM(2,3)
TABLE_SUM(3,0)
TABLE_SUM(3,1)
TABLE_SUM(3,2)
TABLE_SUM(3,3)
TABLE_SUM(4,0)
TABLE_SUM(4,1)
TABLE_SUM(4,2)
TABLE_SUM(4,3)

ACTION_SUM(0,0)
ACTION_SUM(0,1)
ACTION_SUM(0,2)
ACTION_SUM(0,3)
// ACTION_SUM(1,0)
// ACTION_SUM(1,1)
// ACTION_SUM(1,2)
// ACTION_SUM(1,3)
// ACTION_SUM(2,0)
// ACTION_SUM(2,1)
// ACTION_SUM(2,2)
// ACTION_SUM(2,3)
// ACTION_SUM(3,0)
// ACTION_SUM(3,1)
// ACTION_SUM(3,2)
// ACTION_SUM(3,3)
// ACTION_SUM(4,0)
// ACTION_SUM(4,1)
// ACTION_SUM(4,2)
// ACTION_SUM(4,3)

action sum_1_0_action() {
    add(meta.count_0_0_let, meta.count_0_0_let, meta.count_1_0_let);
}
action sum_1_1_action() {
    add(meta.count_0_1_let, meta.count_0_1_let, meta.count_1_1_let);
}
action sum_1_2_action() {
    add(meta.count_0_2_let, meta.count_0_2_let, meta.count_1_2_let);
}
action sum_1_3_action() {
    add(meta.count_0_3_let, meta.count_0_3_let, meta.count_1_3_let);
}

action sum_2_0_action() {
    add(meta.count_0_0_let, meta.count_0_0_let, meta.count_2_0_let);
}
action sum_2_1_action() {
    add(meta.count_0_1_let, meta.count_0_1_let, meta.count_2_1_let);
}
action sum_2_2_action() {
    add(meta.count_0_2_let, meta.count_0_2_let, meta.count_2_2_let);
}
action sum_2_3_action() {
    add(meta.count_0_3_let, meta.count_0_3_let, meta.count_2_3_let);
}

action sum_3_0_action() {
    add(meta.count_0_0_let, meta.count_0_0_let, meta.count_1_0_let);
}
action sum_3_1_action() {
    add(meta.count_0_1_let, meta.count_0_1_let, meta.count_1_1_let);
}
action sum_3_2_action() {
    add(meta.count_0_2_let, meta.count_0_2_let, meta.count_1_2_let);
}
action sum_3_3_action() {
    add(meta.count_0_3_let, meta.count_0_3_let, meta.count_1_3_let);
}

action sum_4_0_action() {
    add(meta.count_0_0_let, meta.count_0_0_let, meta.count_2_0_let);
}
action sum_4_1_action() {
    add(meta.count_0_1_let, meta.count_0_1_let, meta.count_2_1_let);
}
action sum_4_2_action() {
    add(meta.count_0_2_let, meta.count_0_2_let, meta.count_2_2_let);
}
action sum_4_3_action() {
    add(meta.count_0_3_let, meta.count_0_3_let, meta.count_2_3_let);
}

REG_WIN(0,0)
REG_WIN(0,1)
REG_WIN(0,2)
REG_WIN(0,3)
REG_WIN(1,0)
REG_WIN(1,1)
REG_WIN(1,2)
REG_WIN(1,3)
REG_WIN(2,0)
REG_WIN(2,1)
REG_WIN(2,2)
REG_WIN(2,3)
REG_WIN(3,0)
REG_WIN(3,1)
REG_WIN(3,2)
REG_WIN(3,3)
REG_WIN(4,0)
REG_WIN(4,1)
REG_WIN(4,2)
REG_WIN(4,3)