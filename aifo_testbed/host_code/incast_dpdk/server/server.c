#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>
#include <errno.h>
#include <sys/queue.h>
#include <time.h>
#include <assert.h>
#include <arpa/inet.h>
#include <getopt.h>

#include <rte_memory.h>
#include <rte_memzone.h>
#include <rte_launch.h>
#include <rte_eal.h>
#include <rte_per_lcore.h>
#include <rte_lcore.h>
#include <rte_debug.h>
#include <rte_cycles.h>
#include <rte_mbuf.h>
#include <rte_ether.h>
#include <rte_ip.h>
#include <rte_udp.h>
#include <rte_ethdev.h>

#include "util.h"

/*
 * key-value store
 */

uint64_t no_store_value = 0;


uint32_t backend_id = 0;
uint64_t kv_value[VALUE_SIZE];

uint32_t average_interval = 32;

/*
 * functions for processing
 */

int tot_count[10] = {0};

static void process_packet_client(uint32_t lcore_id, struct rte_mbuf *mbuf) {
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];

    // parse packet header
    struct ether_hdr* eth = rte_pktmbuf_mtod(mbuf, struct ether_hdr *);
    struct ipv4_hdr *ip = (struct ipv4_hdr *)((uint8_t*) eth
        + sizeof(struct ether_hdr));
    struct udp_hdr *udp = (struct udp_hdr *)((uint8_t*) ip
        + sizeof(struct ipv4_hdr));

    // parse NetPB header
    MessageHeader* message_header = (MessageHeader*) ((uint8_t *) eth + sizeof(header_template));

    // uint8_t stat_idx = ntohs(udp->dst_port) - 9000;

    uint8_t stat_idx = ntohs(message_header->rank);

    tput_stat[stat_idx].rx += 4 * 8 * (sizeof(MessageHeader) + sizeof(struct udp_hdr) + sizeof(struct ipv4_hdr) + sizeof(struct ether_hdr));
}

// RX loop for test
static int32_t nc_backend_loop(__attribute__((unused)) void *arg) {
    uint32_t lcore_id = rte_lcore_id();
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];
    printf("%lld entering RX loop (master loop) on lcore %u\n", (long long)time(NULL), lcore_id);

    struct rte_mbuf *mbuf;
    struct rte_mbuf *mbuf_burst[NC_MAX_BURST_SIZE];
    uint32_t i, j, nb_rx;
    uint32_t avg_count = 100;
    uint64_t cur_tsc = rte_rdtsc();
    uint64_t update_tsc = rte_get_tsc_hz() / 4; // in second
    uint64_t next_update_tsc = cur_tsc + update_tsc;
    uint64_t adjust_tsc = rte_get_tsc_hz();
    uint64_t next_adjust_tsc = cur_tsc + adjust_tsc;
    uint64_t average_start_tsc = cur_tsc + update_tsc * average_interval;
    uint64_t average_end_tsc = cur_tsc + update_tsc * average_interval * (avg_count + 1);
    // uint64_t average_end_tsc = average_start_tsc + update_tsc * 32;
    uint64_t rx_array[150] = {};
    uint32_t rx_idx = 0;
    while (1) {
        // read current time
        cur_tsc = rte_rdtsc();

        // print stats at master lcore
        if ((lcore_id == rte_get_master_lcore()) && (update_tsc > 0)) {
            if (unlikely(cur_tsc > next_update_tsc)) {
                print_per_core_throughput();
                //print_latency(latency_stat_b);
                next_update_tsc += update_tsc;
            }

            if (unlikely(average_start_tsc > 0 && cur_tsc > average_start_tsc)) {
                uint64_t total_tx = 0;
                uint64_t total_rx = 0;
                uint64_t total_rx_read = 0;
                uint64_t total_rx_write = 0;
                uint64_t total_dropped = 0;

                for (i = 0; i < num_worker; i++) {
                    tput_stat_avg[i].last_tx = tput_stat[i].tx;
                    tput_stat_avg[i].last_rx = tput_stat[i].rx;
                    tput_stat_avg[i].last_rx_read = tput_stat[i].rx_read;
                    tput_stat_avg[i].last_rx_write = tput_stat[i].rx_write;
                    tput_stat_avg[i].last_dropped = tput_stat[i].dropped;

                    total_tx += tput_stat[i].tx;
                    total_rx += tput_stat[i].rx;
                    total_rx_read += tput_stat[i].rx_read;
                    total_rx_write += tput_stat[i].rx_write;
                    total_dropped += tput_stat[i].dropped;
                }
                // tput_stat_avg[0].last_tx = total_tx;
                // tput_stat_avg[0].last_rx = total_rx;
                // tput_stat_avg[0].last_rx_read = total_rx_read;
                // tput_stat_avg[0].last_rx_write = total_rx_write;
                // tput_stat_avg[0].last_dropped = total_dropped;

                average_start_tsc = 0;

            }
            if (unlikely(average_end_tsc > 0 && cur_tsc > average_end_tsc)) {
                uint64_t total_tx = 0;
                uint64_t total_rx = 0;
                uint64_t total_rx_read = 0;
                uint64_t total_rx_write = 0;
                uint64_t total_dropped = 0;
                uint64_t total_latency = 0;
                uint64_t total_latency_num = 0;
                printf("Final! Average!\n");
                for (i = 0; i < num_worker; i++) {
                    tput_stat_avg[i].tx = tput_stat[i].tx;
                    tput_stat_avg[i].rx = tput_stat[i].rx;
                    tput_stat_avg[i].rx_read = tput_stat[i].rx_read;
                    tput_stat_avg[i].rx_write = tput_stat[i].rx_write;
                    tput_stat_avg[i].dropped = tput_stat[i].dropped;
                    // printf("Core %d\n", i);
                    // printf("tx: %"PRIu64"\n", (tput_stat_avg[i].tx - tput_stat_avg[i].last_tx) / average_interval);
                    printf("Core %d;rx: %"PRIu64"\n", i, (tput_stat_avg[i].rx - tput_stat_avg[i].last_rx) / average_interval / avg_count);
                    // printf("rx_read: %"PRIu64"\n", (tput_stat_avg[i].rx_read - tput_stat_avg[i].last_rx_read) / average_interval);
                    // printf("rx_write: %"PRIu64"\n", (tput_stat_avg[i].rx_write - tput_stat_avg[i].last_rx_write) / average_interval);

                    total_tx += tput_stat[i].tx;
                    total_rx += tput_stat[i].rx;
                    total_rx_read += tput_stat[i].rx_read;
                    total_rx_write += tput_stat[i].rx_write;
                    total_dropped += tput_stat[i].dropped;
                }
                // tput_stat_avg[0].tx = total_tx;
                // tput_stat_avg[0].rx = total_rx;
                // tput_stat_avg[0].rx_read = total_rx_read;
                // tput_stat_avg[0].rx_write = total_rx_write;
                // tput_stat_avg[0].dropped = total_dropped;

                uint64_t rx_total = (tput_stat_avg[0].rx - tput_stat_avg[0].last_rx) / average_interval / avg_count;
                // printf("Total\n");
                // printf("tx: %"PRIu64"\n", (tput_stat_avg[0].tx - tput_stat_avg[0].last_tx) / average_interval);
                printf("Total: rx: %"PRIu64"\n", rx_total);
                // printf("rx_read: %"PRIu64"\n", (tput_stat_avg[0].rx_read - tput_stat_avg[0].last_rx_read) / average_interval);
                // printf("rx_write: %"PRIu64"\n", (tput_stat_avg[0].rx_write - tput_stat_avg[0].last_rx_write) / average_interval);
                //printf("dropped: %"PRIu64"\n", (tput_stat_avg.dropped - tput_stat_avg.last_dropped) / average_interval);
                fflush(stdout);

                rx_array[rx_idx] = rx_total;
                rx_idx ++;

                fflush(stdout);

                rte_exit(EXIT_SUCCESS, "Test Completed\n");
            }
        }

        // adjust send limit at master lcore
        if (unlikely(cur_tsc > next_adjust_tsc)) {
            // update_send_limit();
            next_adjust_tsc += adjust_tsc;
        }

        // RX
        for (i = 0; i < lconf->n_rx_queue; i++) {
            // printf("%d, %d\n", lcore_id, lconf->vid);
            nb_rx = rte_eth_rx_burst(lconf->port, lconf->rx_queue_list[i],
                   mbuf_burst, NC_MAX_BURST_SIZE);
            // if (nb_rx > 0)
            //     printf("%d, %d, %d\n", lcore_id, lconf->vid, nb_rx);
            // tput_stat[lconf->vid].rx += nb_rx * 8 * (sizeof(MessageHeader) + sizeof(struct udp_hdr) + sizeof(struct ipv4_hdr) + sizeof(struct ether_hdr));
            // printf("nb_rx: %u, vid: %d\n",nb_rx, lconf->vid);
            for (j = 0; j < nb_rx; j++) {
                mbuf = mbuf_burst[j];
                rte_prefetch0(rte_pktmbuf_mtod(mbuf, void *));
                process_packet_client(lcore_id, mbuf);
                rte_pktmbuf_free(mbuf);
            }
        }
    }
    return 0;
}

// initialization
static void custom_init(void) {
    // initialize per-lcore stats
    memset(&tput_stat, 0, sizeof(tput_stat));
    memset(&kv_value, 0, sizeof(kv_value));

    printf("finish initialization\n");
    printf("==============================\n");
}

/*
 * functions for parsing arguments
 */

static void nc_parse_args_help(void) {
    printf("nc_client [EAL options] --\n"
        "  -p port mask (>0)\n"
        "  -n backend id ([0, 127]\n");
}

static int nc_parse_args(int argc, char **argv) {
    int opt, num;
    double fnum;
    while ((opt = getopt(argc, argv, "p:n:")) != -1) {
        switch (opt) {
        case 'p':
            num = atoi(optarg);
            if (num > 0) {
                enabled_port_mask = num;
            } else {
                nc_parse_args_help();
                return -1;
            }
            break;
        case 'n':
            num = atoi(optarg);
            if (num >= 0 && num <= 127) {
                backend_id = num;
            } else {
                nc_parse_args_help();
                return -1;
            }
            break;
        default:
            nc_parse_args_help();
            return -1;
        }
    }
    printf("parsed arguments: port mask: %"PRIu32
        ", backend id: %"PRIu32
        "\n",
        enabled_port_mask, backend_id);
    return 1;
}


/*
 * main function
 */

int main(int argc, char **argv) {
    int ret;
    uint32_t lcore_id;

    // parse default arguments
    ret = rte_eal_init(argc, argv);
    if (ret < 0) {
        rte_exit(EXIT_FAILURE, "invalid EAL arguments\n");
    }
    argc -= ret;
    argv += ret;

    // parse netcache arguments
    ret = nc_parse_args(argc, argv);
    if (ret < 0) {
        rte_exit(EXIT_FAILURE, "invalid netcache arguments\n");
    }

    nc_init();
    custom_init();

    // launch main loop in every lcore
    rte_eal_mp_remote_launch(nc_backend_loop, NULL, CALL_MASTER);
    // rte_eal_mp_remote_launch(np_client_rx_loop, NULL, CALL_MASTER);
    RTE_LCORE_FOREACH_SLAVE(lcore_id) {
        if (rte_eal_wait_lcore(lcore_id) < 0) {
            ret = -1;
            break;
        }
    }

    return 0;
}
