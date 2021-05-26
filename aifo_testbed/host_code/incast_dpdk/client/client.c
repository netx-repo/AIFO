#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
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
 * global variables
 */

uint8_t print_flag = 0;
uint32_t write_ratio = 0;
uint64_t pkts_send_limit_ms = 10000;

char ip_client[][32] = {
    "10.1.0.0",
    "10.1.0.1",
    "10.1.0.2",
    "10.1.0.3",
    "10.1.0.4",
    "10.1.0.5",
    "10.1.0.6",
    "10.1.0.7",
    "10.1.0.8",
    "10.1.0.9",
    "10.1.0.10",
    "10.1.0.11",
    "10.1.0.12"
    };

char ip_server[][32] = {
    "10.1.0.0",
    "10.1.0.1",
    "10.1.0.2",
    "10.1.0.3",
    "10.1.0.4",
    "10.1.0.5",
    "10.1.0.6",
    "10.1.0.7",
    "10.1.0.8",
    "10.1.0.9",
    "10.1.0.10",
    "10.1.0.11",
    "10.1.0.12"
    };

uint32_t pkt_size = 90;
uint64_t write_value = 1234;
uint32_t client_idx = 1;
uint32_t tenant_idx = 1;

uint32_t server_idx = 8;
uint32_t dst_port = 9000;
uint32_t time_to_run = 3000;

uint32_t rank = 0;
/*
 * functions for processing
 */
uint8_t counter[10] = {0};
// generate request packet TODO
static void generate_request_pkt(uint32_t lcore_id, struct rte_mbuf *mbuf, uint64_t pkts_send_ms) {
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];
    assert(mbuf != NULL);

    // init packet header
    struct ether_hdr* eth = rte_pktmbuf_mtod(mbuf, struct ether_hdr *);
    struct ipv4_hdr *ip = (struct ipv4_hdr *)((uint8_t*) eth
        + sizeof(struct ether_hdr));
    struct udp_hdr *udp = (struct udp_hdr *)((uint8_t*) ip
        + sizeof(struct ipv4_hdr));
    rte_memcpy(eth, header_template, sizeof(header_template));
    mbuf->data_len = sizeof(header_template) + sizeof(MessageHeader);
    mbuf->pkt_len = sizeof(header_template) + sizeof(MessageHeader);
    mbuf->next = NULL;
    mbuf->nb_segs = 1;
    mbuf->ol_flags = 0;

    inet_pton(AF_INET, ip_client[client_idx], &(ip->src_addr));
    inet_pton(AF_INET, ip_server[server_idx], &(ip->dst_addr));
    udp->src_port = htons(1234);
    // udp->dst_port = htons(dst_port + lcore_id - 1);
    udp->dst_port = htons(dst_port + 1 - 1);
    
    MessageHeader* message_header = (MessageHeader*) ((uint8_t*)eth + sizeof(header_template));

    rank = client_idx;
    // key
    message_header->rank = htons(rank);
}

int64_t max(uint64_t p, uint64_t q) {
    if (p>q)
        return p;
    return q;
}

// TX loop for test
static int32_t nc_test_tx_loop(uint32_t lcore_id) {
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];
    printf("%lld entering main loop on lcore %u mode TX\n", (long long)time(NULL), lcore_id);

    struct rte_mbuf *mbuf;

    uint64_t cur_tsc = rte_rdtsc();
    uint64_t update_tsc = rte_get_tsc_hz(); // in second
    uint64_t next_update_tsc = cur_tsc + update_tsc;
    uint64_t ms_tsc = rte_get_tsc_hz() / 10000;
    uint64_t next_ms_tsc = cur_tsc + ms_tsc;
    uint64_t drain_tsc = (rte_get_tsc_hz() + US_PER_S - 1) / US_PER_S * 10;
    uint64_t next_drain_tsc = cur_tsc + drain_tsc;
    uint64_t pkts_send_ms = 0;
    uint64_t last_pkts_send_ms = 0;
    uint64_t finish_tsc = rte_rdtsc() + rte_get_tsc_hz() * time_to_run;

    while (1) {
        // read current time
        cur_tsc = rte_rdtsc();

        // if (unlikely(cur_tsc > finish_tsc)) {
        //     break;
        // }

        // print stats at master lcore
        if (update_tsc > 0) {
            if (unlikely(cur_tsc > next_update_tsc)) {
                if (lcore_id == rte_get_master_lcore()) {
                    print_per_core_throughput();
                }
                next_update_tsc += update_tsc;
            }
        }

        // clean packet counters for each ms
        if (unlikely(cur_tsc > next_ms_tsc)) {
            last_pkts_send_ms = pkts_send_ms;
            pkts_send_ms = 0;
            next_ms_tsc += ms_tsc;
        }

        // TX: send packets, drain TX queue
        if (unlikely(cur_tsc > next_drain_tsc)) {
            send_pkt_burst(lcore_id);
            next_drain_tsc += drain_tsc;
        }

        // TX: generate packet, put in TX queue
        if ((cur_tsc <= finish_tsc) && (pkts_send_ms < pkts_send_limit_ms)) {
            mbuf = rte_pktmbuf_alloc(pktmbuf_pool);
            generate_request_pkt(lcore_id, mbuf, max(last_pkts_send_ms, pkts_send_ms));
            enqueue_pkt(lcore_id, mbuf);
            pkts_send_ms++;
        }
    }
    return 0;
}

static int32_t nc_test_master_loop(uint32_t lcore_id) {
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];
    printf("%lld entering main loop on lcore %u mode TX\n", (long long)time(NULL), lcore_id);

    struct rte_mbuf *mbuf;

    uint64_t cur_tsc = rte_rdtsc();
    uint64_t update_tsc = rte_get_tsc_hz(); // in second
    uint64_t next_update_tsc = cur_tsc + update_tsc;
    uint64_t ms_tsc = rte_get_tsc_hz() / 1000;
    uint64_t next_ms_tsc = cur_tsc + ms_tsc;
    uint64_t drain_tsc = (rte_get_tsc_hz() + US_PER_S - 1) / US_PER_S * 10;
    uint64_t next_drain_tsc = cur_tsc + drain_tsc;
    uint64_t pkts_send_ms = 0;


    while (1) {
        // read current time
        cur_tsc = rte_rdtsc();

        // print stats at master lcore
        if (update_tsc > 0) {
            if (unlikely(cur_tsc > next_update_tsc)) {
                if (lcore_id == rte_get_master_lcore()) {
                    print_per_core_throughput();
                }
                next_update_tsc += update_tsc;
            }
        }

    }
    return 0;
}

// main processing loop for client
static int32_t client_loop(__attribute__((unused)) void *arg) {
    uint32_t lcore_id = rte_lcore_id();
    if (lcore_id > 0) {
    nc_test_tx_loop(lcore_id);
    }
    else {
    nc_test_master_loop(lcore_id);
    }
    return 0;
}


/*
 * functions for parsing arguments
 */

static void nc_parse_args_help(void) {
    printf("simple_socket [EAL options] --\n"
        "  -w write_ratio (0-100)\n"
        "  -s pkts_per_ms (>0)\n");
}

static int nc_parse_args(int argc, char **argv) {
    int opt, num;
    double fnum;
    while ((opt = getopt(argc, argv, "s:n:r:t:p:T:")) != -1) {
        switch (opt) {
            case 's':
                num = atoi(optarg);
                pkts_send_limit_ms = num;
                break;
            case 'n':
                num = atoi(optarg);
                client_idx = num;
                break;
            case 't':
                num = atoi(optarg);
                tenant_idx = num;
                break;
            case 'r':
                num = atoi(optarg);
                server_idx = num;
                break;
            case 'p':
                num = atoi(optarg);
                dst_port = num;
                break;
            case 'T':
                num = atoi(optarg);
                time_to_run = num;
                break;
            default:
                nc_parse_args_help();
                return -1;
        }
    }
    return 1;
}

/*
 * main function
 */

int main(int argc, char **argv) {
    int ret;
    uint32_t lcore_id;
    uint32_t pktsize;
    pktsize = sizeof(MessageHeader) + sizeof(struct udp_hdr) + sizeof(struct ipv4_hdr) + sizeof(struct ether_hdr);
    printf("Packet size:%d\n", pktsize);
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

    // init
    nc_init();
    // custom_init();

    rte_eal_mp_remote_launch(client_loop, NULL, CALL_MASTER);

    RTE_LCORE_FOREACH_SLAVE(lcore_id) {
        if (rte_eal_wait_lcore(lcore_id) < 0) {
            ret = -1;
            break;
        }
    }

    return 0;
}
