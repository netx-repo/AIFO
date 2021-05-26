package ch.ethz.systems.netbench.xpt.simple.simpleudp;

import ch.ethz.systems.netbench.ext.basic.TcpPacket;

public class SimpleUdpPacket extends TcpPacket {
//    public SimpleUdpPacket(long flowId, long dataSizeByte, int sourceId, int destinationId, int TTL, int sourcePort, int destinationPort, long sequenceNumber, long acknowledgementNumber, boolean NS, boolean CWR, boolean ECE, boolean URG, boolean ACK, boolean PSH, boolean RST, boolean SYN, boolean FIN, double windowSize) {
//        super(flowId, dataSizeByte, sourceId, destinationId, TTL, sourcePort, destinationPort, sequenceNumber, acknowledgementNumber, NS, CWR, ECE, URG, ACK, PSH, RST, SYN, FIN, windowSize);
//    }
    SimpleUdpPacket(long flowId, long dataSizeByte, int sourceId, int destinationId, long sequenceNumber, long acknowledgementNumber, boolean ECE, boolean ACK, double windowSize) {
        super(
                flowId,
                dataSizeByte,
                sourceId,
                destinationId,
                0,
                0,
                0,
                sequenceNumber,
                acknowledgementNumber,
                false,
                false,
                ECE,
                false,
                ACK,
                false,
                false,
                false,
                false,
                windowSize
        );
    }
}
