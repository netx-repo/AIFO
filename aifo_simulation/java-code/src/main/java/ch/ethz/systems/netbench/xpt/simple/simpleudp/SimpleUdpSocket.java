package ch.ethz.systems.netbench.xpt.simple.simpleudp;


import ch.ethz.systems.netbench.core.Simulator;
import ch.ethz.systems.netbench.core.log.SimulationLogger;
import ch.ethz.systems.netbench.core.network.Packet;
import ch.ethz.systems.netbench.core.network.Socket;
import ch.ethz.systems.netbench.core.network.TransportLayer;
import ch.ethz.systems.netbench.core.network.UDPSendPacketEvent;
import ch.ethz.systems.netbench.ext.basic.TcpPacket;
import ch.ethz.systems.netbench.xpt.tcpbase.FullExtTcpPacket;
import ch.ethz.systems.netbench.xpt.tcpbase.TcpLogger;

import java.util.Random;
// **TODO change to UdpPacket
public class SimpleUdpSocket extends Socket {

    private static final long MAX_SEGMENT_SIZE = 1380L / 4;

    private long sendNextNumber;
    private double congestionWindow;
    private TcpLogger logger;

    public SimpleUdpSocket(TransportLayer transportLayer, long flowId, int sourceId, int destinationId, long flowSizeByte) {
        super(transportLayer, flowId, sourceId, destinationId, flowSizeByte);
        this.logger = new TcpLogger(flowId, flowSizeByte == -1);
        this.congestionWindow = 3 * 1380;
        this.sendNextNumber = 0;
    }

    public SimpleUdpSocket(TransportLayer transportLayer, long flowId, int sourceId, int destinationId, long flowSizeByte, long realFlowSizeByte) {
        super(transportLayer, flowId, sourceId, destinationId, flowSizeByte, true, realFlowSizeByte, 80, 80);
        this.logger = new TcpLogger(flowId, flowSizeByte == -1);
        this.congestionWindow = 3 * 1380;
        this.sendNextNumber = 0;
    }

    public SimpleUdpSocket(TransportLayer transportLayer, long flowId, int sourceId, int destinationId, long flowSizeByte, int sourcePort, int destinationPort) {
        super(transportLayer, flowId, sourceId, destinationId, flowSizeByte, sourcePort, destinationPort);
        this.logger = new TcpLogger(flowId, flowSizeByte == -1);
        this.congestionWindow = 3 * 1380;
        this.sendNextNumber = 0;
    }

    public SimpleUdpSocket(TransportLayer transportLayer, long flowId, int sourceId, int destinationId, long flowSizeByte, long realFlowSizeByte, int sourcePort, int destinationPort) {
        super(transportLayer, flowId, sourceId, destinationId, flowSizeByte, true, realFlowSizeByte, sourcePort, destinationPort);
        this.logger = new TcpLogger(flowId, flowSizeByte == -1);
        this.congestionWindow = 3 * 1380;
        this.sendNextNumber = 0;
    }

    @java.lang.Override
    public void start() {
        Random rand = new Random();
        int random_integer = rand.nextInt(470000-10000) + 10000;
        boolean flag;

        flag = sendOutPendingData();
        if (flag == true) {
            Simulator.registerEvent(new UDPSendPacketEvent(12000 / 4 * 10 * 4, this));
            // * for rack-scale
            // Simulator.registerEvent(new UDPSendPacketEvent(12000 / 40 * 19, this));
        }

    }

    @java.lang.Override
    public void handle(Packet genericPacket) {
//        TcpPacket packet = (TcpPacket) genericPacket;
        FullExtTcpPacket packet = (FullExtTcpPacket) genericPacket;
        long size = packet.getDataSizeByte();

        if (this.isReceiver()) {
            // ** confirm UDP packet
            this.confirmFlowUdp(size);
        }
    }

    private boolean sendOutPendingData() {
        long amountToSendByte = getFlowSizeByteBySeq(sendNextNumber);
        long seq = sendNextNumber;
        sendNextNumber += amountToSendByte;

//        sendWithoutResend(new SimpleUdpPacket(flowId, amountToSendByte, sourceId, destinationId, seq, 0, false, false, congestionWindow));
        sendWithoutResend(createPacket(
                amountToSendByte, // Data size (byte)
                sendNextNumber, // Seq number
                0, // Ack number
                false, // ACK
                true,  // SYN
                false  // ECE
        ));
        if (seq >= flowSizeByte)
            return false;
        else
            return true;
    }

    private void sendWithoutResend(FullExtTcpPacket packet) {
        SimulationLogger.increaseStatisticCounter("NO_RESEND_PACKETS_SENT");

        transportLayer.send(packet);
    }

    private long getFlowSizeByteBySeq(long seq) {
        return Math.min(MAX_SEGMENT_SIZE, flowSizeByte - seq);
    }

    private FullExtTcpPacket createPacket(
            long dataSizeByte,
            long sequenceNumber,
            long ackNumber,
            boolean ACK,
            boolean SYN,
            boolean ECE
    ) {
        return new FullExtTcpPacket(
                flowId, dataSizeByte, sourceId, destinationId,
                100, this.getSourcePort(), this.getDestinationPort(), // TTL, source port, destination port
                sequenceNumber, ackNumber, // Seq number, Ack number
                false, false, ECE, // NS, CWR, ECE
                false, ACK, false, // URG, ACK, PSH
                false, SYN, false, // RST, SYN, FIN
                congestionWindow, 2000000000, // Window size, Priority
                flowSizeByte
        );
    }
}
