#ifndef NETCACHE_UTIL_H
#define NETCACHE_UTIL_H

/*
 * constants
 */

#define NC_MAX_PAYLOAD_SIZE     1500
#define NC_NB_MBUF              8191
#define NC_MBUF_SIZE            (2048+sizeof(struct rte_mbuf)+RTE_PKTMBUF_HEADROOM)
#define NC_MBUF_CACHE_SIZE      32
#define NC_MAX_BURST_SIZE       32
#define NC_MAX_LCORES           32
#define NC_NB_RXD               128 // RX descriptors
#define NC_NB_TXD               512 // TX descriptors
#define NC_RX_QUEUE_PER_LCORE   4
#define NC_DRAIN_US             10

#define TYPE_GET_REQUEST            0x01
#define TYPE_PUT_REQUEST            0x02
#define TYPE_DEL_REQUEST            0x03
#define TYPE_GET_RESPONSE_C         0x04
#define TYPE_PUT_RESPONSE_C         0x05
#define TYPE_DEL_RESPONSE_C         0x06
#define TYPE_GET_RESPONSE_B         0x07
#define TYPE_PUT_RESPONSE_B         0x08
#define TYPE_DEL_RESPONSE_B         0x09
#define TYPE_WRITE_CACHED           0x12
#define TYPE_DELETE_CACHED          0x13
#define TYPE_CACHE_UPDATE           0x14
#define TYPE_CACHE_UPDATE_RESPONSE  0x15
#define TYPE_HOT_READ               0x16
#define TYPE_RESET_COUNTER          0x20

#define NODE_NUM                128
#define IP_SRC                  "192.168.11.1"
#define CLIENT_SLAVE_IP         "192.168.11.2"
#define IP_DST                  "192.168.12.1"
#define CLIENT_PORT             8887
#define SERVICE_PORT            8888
#define KEY_SPACE_SIZE          1000000
#define PER_NODE_KEY_SPACE_SIZE (KEY_SPACE_SIZE / NODE_NUM)
#define BIN_SIZE                100
#define BIN_RANGE               10
#define BIN_MAX                 (BIN_SIZE * BIN_RANGE)

#define TRACE_LENGTH            (1000*1000*10)
#define SIMULATION_LENGTH       (1000*1000*10)
#define VALUE_SIZE              16
#define CACHE_SIZE              10000

#define CHANGE_SIZE             200
#define CHANGE_INTERVAL         10
#define CHANGE_PATTERN          0

#define CONTROLLER_IP           "10.201.124.31"
#define CONTROLLER_PORT         8890
#define CLIENT_MASTER_IP        "127.0.0.1"
#define CLIENT_MASTER_PORT      8891

static const struct rte_eth_conf port_conf = {
    .rxmode = {
        //.mq_mode = ETH_MQ_RX_RSS,
        .max_rx_pkt_len = ETHER_MAX_LEN,
        .split_hdr_size = 0,
        .header_split   = 0, // Header Split disabled
        .hw_ip_checksum = 0, // IP checksum offload disabled
        .hw_vlan_filter = 0, // VLAN filtering disabled
        .jumbo_frame    = 0, // Jumbo Frame Support disabled
        .hw_strip_crc   = 0, // CRC stripped by hardware
    },
    /*.rx_adv_conf = {
        .rss_conf = {
            .rss_key = NULL,
            .rss_hf = ETH_RSS_IP,
        },
    },*/
    .txmode = {
        .mq_mode = ETH_MQ_TX_NONE,
    },
};

/*
 * custom types
 */

typedef struct MessageHeader_ {
    uint32_t rank;
    // uint32_t qid;
    
    uint64_t fill_pkt_len1[50];
} __attribute__((__packed__)) MessageHeader;

struct mbuf_table {
    uint32_t len;
    struct rte_mbuf *m_table[NC_MAX_BURST_SIZE];
};

struct lcore_configuration {
    uint32_t vid; // virtual core id
    uint32_t port; // one port
    uint32_t tx_queue_id; // one TX queue
    uint32_t n_rx_queue;  // number of RX queues
    uint32_t rx_queue_list[NC_RX_QUEUE_PER_LCORE]; // list of RX queues
    struct mbuf_table tx_mbufs; // mbufs to hold TX queue
} __rte_cache_aligned;

struct throughput_statistics {
    uint64_t tx;
    uint64_t rx_c;
    uint64_t rx;
    uint64_t dropped;
    uint64_t last_tx;
    uint64_t last_rx_c;
    uint64_t last_rx;
    uint64_t last_dropped;
} __rte_cache_aligned;

/*
 * global variables
 */

uint32_t enabled_port_mask = 1;
uint32_t enabled_ports[RTE_MAX_ETHPORTS];
uint32_t n_enabled_ports = 0;
uint32_t n_rx_queues = 0;
uint32_t n_lcores = 0;

struct rte_mempool *pktmbuf_pool = NULL;
struct ether_addr port_eth_addrs[RTE_MAX_ETHPORTS];
struct lcore_configuration lcore_conf[NC_MAX_LCORES];
struct throughput_statistics tput_stat[NC_MAX_LCORES];

uint8_t header_template[
    sizeof(struct ether_hdr)
    + sizeof(struct ipv4_hdr)
    + sizeof(struct udp_hdr)];

/*
 * functions for generation
 */

// send packets, drain TX queue
static void send_pkt_burst(uint32_t lcore_id) {
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];
    struct rte_mbuf **m_table = (struct rte_mbuf **)lconf->tx_mbufs.m_table;

    uint32_t n = lconf->tx_mbufs.len;
    uint32_t ret = rte_eth_tx_burst(
        lconf->port,
        lconf->tx_queue_id,
        m_table,
        lconf->tx_mbufs.len);
    tput_stat[lconf->vid].tx += ret * 8 * (sizeof(MessageHeader) + sizeof(struct udp_hdr) + sizeof(struct ipv4_hdr) + sizeof(struct ether_hdr));
    if (unlikely(ret < n)) {
        tput_stat[lconf->vid].dropped += (n - ret);
        do {
            rte_pktmbuf_free(m_table[ret]);
        } while (++ret < n);
    }
    lconf->tx_mbufs.len = 0;
}

// put packet into TX queue
static void enqueue_pkt(uint32_t lcore_id, struct rte_mbuf *mbuf) {
    struct lcore_configuration *lconf = &lcore_conf[lcore_id];
    lconf->tx_mbufs.m_table[lconf->tx_mbufs.len++] = mbuf;

    // enough packets in TX queue
    if (unlikely(lconf->tx_mbufs.len == NC_MAX_BURST_SIZE)) {
        send_pkt_burst(lcore_id);
    }
}

/*
 * functions for initialization
 */

// init header template
static void init_header_template(void) {
    memset(header_template, 0, sizeof(header_template));
    struct ether_hdr *eth = (struct ether_hdr *)header_template;
    struct ipv4_hdr *ip = (struct ipv4_hdr *)((uint8_t*) eth + sizeof(struct ether_hdr));
    struct udp_hdr *udp = (struct udp_hdr *)((uint8_t*)ip + sizeof(struct ipv4_hdr));
    uint32_t pkt_len = sizeof(header_template) + sizeof(MessageHeader);

    // eth header
    eth->ether_type = rte_cpu_to_be_16(ETHER_TYPE_IPv4);
    struct ether_addr src_addr = {
        .addr_bytes = {0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff}};
    struct ether_addr dst_addr = {
        .addr_bytes = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55}};
    //ether_addr_copy(&port_eth_addrs[0], &eth->s_addr);
    ether_addr_copy(&src_addr, &eth->s_addr);
    ether_addr_copy(&dst_addr, &eth->d_addr);

    // ip header
    char src_ip[] = IP_SRC;
    char dst_ip[] = IP_DST;
    int st1 = inet_pton(AF_INET, src_ip, &(ip->src_addr));
    int st2 = inet_pton(AF_INET, dst_ip, &(ip->dst_addr));
    if(st1 != 1 || st2 != 1) {
        fprintf(stderr, "inet_pton() failed.Error message: %s %s",
            strerror(st1), strerror(st2));
        exit(EXIT_FAILURE);
    }
    ip->total_length = rte_cpu_to_be_16(pkt_len - sizeof(struct ether_hdr));
    ip->version_ihl = 0x45;
    ip->type_of_service = 0;
    ip->packet_id = 0;
    ip->fragment_offset = 0;
    ip->time_to_live = 64;
    ip->next_proto_id = IPPROTO_UDP;
    uint32_t ip_cksum;
    uint16_t *ptr16 = (uint16_t *)ip;
    ip_cksum = 0;
    ip_cksum += ptr16[0]; ip_cksum += ptr16[1];
    ip_cksum += ptr16[2]; ip_cksum += ptr16[3];
    ip_cksum += ptr16[4];
    ip_cksum += ptr16[6]; ip_cksum += ptr16[7];
    ip_cksum += ptr16[8]; ip_cksum += ptr16[9];
    ip_cksum = ((ip_cksum & 0xffff0000) >> 16) + (ip_cksum & 0x0000ffff);
    if (ip_cksum > 65535) {
        ip_cksum -= 65535;
    }
    ip_cksum = (~ip_cksum) & 0x0000ffff;
    if (ip_cksum == 0) {
        ip_cksum = 0xffff;
    }
    ip->hdr_checksum = (uint16_t)ip_cksum;

    // udp header
    udp->src_port = htons(CLIENT_PORT);
    udp->dst_port = htons(SERVICE_PORT);
    udp->dgram_len = rte_cpu_to_be_16(pkt_len
        - sizeof(struct ether_hdr)
        - sizeof(struct ipv4_hdr));
    udp->dgram_cksum = 0;
}

// check link status
static void check_link_status(void) {
    const uint32_t check_interval_ms = 100;
    const uint32_t check_iterations = 90;
    uint32_t i, j;
    struct rte_eth_link link;
    for (i = 0; i < check_iterations; i++) {
        uint8_t all_ports_up = 1;
        for (j = 0; j < n_enabled_ports; j++) {
            uint32_t portid = enabled_ports[j];
            memset(&link, 0, sizeof(link));
            rte_eth_link_get_nowait(portid, &link);
            if (link.link_status) {
                printf("\tport %u link up - speed %u Mbps - %s\n",
                    portid,
                    link.link_speed,
                    (link.link_duplex == ETH_LINK_FULL_DUPLEX) ?
                        "full-duplex" : "half-duplex");
            } else {
                all_ports_up = 0;
            }
        }

        if (all_ports_up == 1) {
            printf("check link status finish: all ports are up\n");
            break;
        } else if (i == check_iterations - 1) {
            printf("check link status finish: not all ports are up\n");
        } else {
            rte_delay_ms(check_interval_ms);
        }
    }
}

// initialize all status
static void nc_init(void) {
    uint32_t i, j;

    // create mbuf pool
    printf("create mbuf pool\n");
    pktmbuf_pool = rte_mempool_create(
        "mbuf_pool",
        NC_NB_MBUF,
        NC_MBUF_SIZE,
        NC_MBUF_CACHE_SIZE,
        sizeof(struct rte_pktmbuf_pool_private),
        rte_pktmbuf_pool_init, NULL,
        rte_pktmbuf_init, NULL,
        rte_socket_id(),
        0);
    if (pktmbuf_pool == NULL) {
        rte_exit(EXIT_FAILURE, "cannot init mbuf pool\n");
    }

    // determine available ports
    printf("create enabled ports\n");
    uint32_t n_total_ports = 0;
    n_total_ports = rte_eth_dev_count();
    if (n_total_ports == 0) {
      rte_exit(EXIT_FAILURE, "cannot detect ethernet ports\n");
    }
    if (n_total_ports > RTE_MAX_ETHPORTS) {
        n_total_ports = RTE_MAX_ETHPORTS;
    }

    // get info for each enabled port
    struct rte_eth_dev_info dev_info;
    n_enabled_ports = 0;
    printf("\tports: ");
    for (i = 0; i < n_total_ports; i++) {
        if ((enabled_port_mask & (1 << i)) == 0) {
            continue;
        }
        enabled_ports[n_enabled_ports++] = i;
        rte_eth_dev_info_get(i, &dev_info);
        printf("%u ", i);
    }
    printf("\n");

    // find number of active lcores
    printf("create enabled cores\n\tcores: ");
    n_lcores = 0;
    for(i = 0; i < NC_MAX_LCORES; i++) {
        if(rte_lcore_is_enabled(i)) {
            n_lcores++;
            printf("%u ",i);
        }
    }
    printf("\n");

    // ensure numbers are correct
    if (n_lcores % n_enabled_ports != 0) {
        rte_exit(EXIT_FAILURE,
            "number of cores (%u) must be multiple of ports (%u)\n",
            n_lcores, n_enabled_ports);
    }

    uint32_t rx_queues_per_lcore = NC_RX_QUEUE_PER_LCORE;
    uint32_t rx_queues_per_port = rx_queues_per_lcore * n_lcores / n_enabled_ports;
    uint32_t tx_queues_per_port = n_lcores / n_enabled_ports;

    if (rx_queues_per_port < rx_queues_per_lcore) {
        rte_exit(EXIT_FAILURE,
            "rx_queues_per_port (%u) must be >= rx_queues_per_lcore (%u)\n",
            rx_queues_per_port, rx_queues_per_lcore);
    }

    // assign each lcore some RX queues and a port
    printf("set up %d RX queues per port and %d TX queues per port\n",
        rx_queues_per_port, tx_queues_per_port);
    uint32_t portid_offset = 0;
    uint32_t rx_queue_id = 0;
    uint32_t tx_queue_id = 0;
    uint32_t vid = 0;
    for (i = 0; i < NC_MAX_LCORES; i++) {
        if(rte_lcore_is_enabled(i)) {
            lcore_conf[i].vid = vid++;
            lcore_conf[i].n_rx_queue = rx_queues_per_lcore;
            for (j = 0; j < rx_queues_per_lcore; j++) {
                lcore_conf[i].rx_queue_list[j] = rx_queue_id++;
            }
            lcore_conf[i].port = enabled_ports[portid_offset];
            lcore_conf[i].tx_queue_id = tx_queue_id++;
            if (rx_queue_id % rx_queues_per_port == 0) {
                portid_offset++;
                rx_queue_id = 0;
                tx_queue_id = 0;
            }
        }
    }

    // initialize each port
    for (portid_offset = 0; portid_offset < n_enabled_ports; portid_offset++) {
        uint32_t portid = enabled_ports[portid_offset];

        int32_t ret = rte_eth_dev_configure(portid, rx_queues_per_port,
            tx_queues_per_port, &port_conf);
        if (ret < 0) {
            rte_exit(EXIT_FAILURE, "cannot configure device: err=%d, port=%u\n",
               ret, portid);
        }
        rte_eth_macaddr_get(portid, &port_eth_addrs[portid]);

        // initialize RX queues
        for (i = 0; i < rx_queues_per_port; i++) {
            ret = rte_eth_rx_queue_setup(portid, i, NC_NB_RXD,
                rte_eth_dev_socket_id(portid), NULL, pktmbuf_pool);
            if (ret < 0) {
                rte_exit(EXIT_FAILURE,
                    "rte_eth_rx_queue_setup: err=%d, port=%u\n", ret, portid);
            }
         }

        // initialize TX queues
        for (i = 0; i < tx_queues_per_port; i++) {
            ret = rte_eth_tx_queue_setup(portid, i, NC_NB_TXD,
                rte_eth_dev_socket_id(portid), NULL);
            if (ret < 0) {
                rte_exit(EXIT_FAILURE,
                    "rte_eth_tx_queue_setup: err=%d, port=%u\n", ret, portid);
            }
        }

        // start device
        ret = rte_eth_dev_start(portid);
        if (ret < 0) {
            rte_exit(EXIT_FAILURE,
                "rte_eth_dev_start: err=%d, port=%u\n", ret, portid);
        }

        rte_eth_promiscuous_enable(portid);

        char mac_buf[ETHER_ADDR_FMT_SIZE];
        ether_format_addr(mac_buf, ETHER_ADDR_FMT_SIZE, &port_eth_addrs[portid]);
        printf("initiaze queues and start port %u, MAC address:%s\n",
           portid, mac_buf);
    }

    if (!n_enabled_ports) {
        rte_exit(EXIT_FAILURE, "all available ports are disabled. Please set portmask.\n");
    }
    check_link_status();
    init_header_template();
}

/*
 * functions for print
 */

// print current time
static void print_time(void) {
    time_t timer;
    char buffer[26];
    struct tm* tm_info;
    time(&timer);
    tm_info = localtime(&timer);
    strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);
    printf("%s\n", buffer);
}

// print packet
static void print_packet(struct rte_mbuf *mbuf) {
    // print length
    printf("packet: pkt_len:%"PRIu32" data_len:%"PRIu16"\n", mbuf->pkt_len, mbuf->data_len);

    // print eth
    struct ether_hdr* eth = rte_pktmbuf_mtod(mbuf, struct ether_hdr *);
    char mac_buf[ETHER_ADDR_FMT_SIZE];
    ether_format_addr(mac_buf, ETHER_ADDR_FMT_SIZE, &eth->s_addr);
    printf("\teth: src_mac:%s", mac_buf);
    ether_format_addr(mac_buf, ETHER_ADDR_FMT_SIZE, &eth->d_addr);
    printf(" dst_mac:%s\n", mac_buf);

    // print ip
    struct ipv4_hdr* ip = (struct ipv4_hdr*) ((uint8_t*)eth + sizeof(struct ether_hdr));
    char ip_buf[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &ip->src_addr, ip_buf, INET_ADDRSTRLEN);
    printf("\tip: src_ip:%s", ip_buf);
    inet_ntop(AF_INET, &ip->dst_addr, ip_buf, INET_ADDRSTRLEN);
    printf(" dst_ip:%s\n", ip_buf);

    // print payload
    MessageHeader* message_header = (MessageHeader*) ((uint8_t*)eth + sizeof(header_template));
    
    /*uint8_t* value = (uint8_t *) eth
        + sizeof(header_template) + sizeof(MessageHeader);
    uint32_t i;
    for (i = 0; i < VALUE_SIZE; i++) {
        printf("%"PRIu64" ", *((uint64_t*)(value + i * 8)));
    }
    printf("\n");*/
}

// print per-core throughput
static void print_per_core_throughput(void) {
    // time is in second
    printf("%lld\nthroughput\n", (long long)time(NULL));
    uint32_t i;
    uint64_t total_tx = 0;
    uint64_t total_rx_c = 0;
    uint64_t total_rx = 0;
    uint64_t total_dropped = 0;
    for (i = 0; i < n_lcores; i++) {
        printf("\tcore %"PRIu32"\t"
            "tx: %"PRIu64"\t"
            "rx_c: %"PRIu64"\t"
            "rx: %"PRIu64"\t"
            "dropped: %"PRIu64"\n",
            i, (tput_stat[i].tx - tput_stat[i].last_tx),
            tput_stat[i].rx_c - tput_stat[i].last_rx_c,
            tput_stat[i].rx - tput_stat[i].last_rx,
            tput_stat[i].dropped - tput_stat[i].last_dropped);
        total_tx += tput_stat[i].tx - tput_stat[i].last_tx;
        total_rx_c += tput_stat[i].rx_c - tput_stat[i].last_rx_c;
        total_rx += tput_stat[i].rx - tput_stat[i].last_rx;
        total_dropped += tput_stat[i].dropped - tput_stat[i].last_dropped;
        tput_stat[i].last_tx = tput_stat[i].tx;
        tput_stat[i].last_rx_c = tput_stat[i].rx_c;
        tput_stat[i].last_rx = tput_stat[i].rx;
        tput_stat[i].last_dropped = tput_stat[i].dropped;
    }
    printf("\ttotal\ttx: %"PRIu64"\t"
        "rx_c: %"PRIu64"\t"
        "rx: %"PRIu64"\t"
        "dropped: %"PRIu64"\n",
        total_tx, total_rx_c, total_rx, total_dropped);
    fflush(stdout);
}

// print throughput
static void print_throughput(void) {
    // time is in second
    printf("%lld\nthroughput ", (long long)time(NULL));
    uint32_t i;
    uint64_t total_tx = 0;
    uint64_t total_rx_c = 0;
    uint64_t total_rx = 0;
    uint64_t total_dropped = 0;
    for (i = 0; i < n_lcores; i++) {
        total_tx += tput_stat[i].tx - tput_stat[i].last_tx;
        total_rx_c += tput_stat[i].rx_c - tput_stat[i].last_rx_c;
        total_rx += tput_stat[i].rx - tput_stat[i].last_rx;
        total_dropped += tput_stat[i].dropped - tput_stat[i].last_dropped;
        tput_stat[i].last_tx = tput_stat[i].tx;
        tput_stat[i].last_rx_c = tput_stat[i].rx_c;
        tput_stat[i].last_rx = tput_stat[i].rx;
        tput_stat[i].last_dropped = tput_stat[i].dropped;
    }
    printf("tx: %"PRIu64"\t"
        "rx_c: %"PRIu64"\t"
        "rx: %"PRIu64"\t"
        "dropped: %"PRIu64"\n",
        total_tx, total_rx_c, total_rx, total_dropped);
}

/*
 * misc
 */

static uint64_t timediff_in_us(uint64_t new_t, uint64_t old_t) {
    return (new_t - old_t) * 1000000UL / rte_get_tsc_hz();
}

#endif //NETCACHE_UTIL_H
