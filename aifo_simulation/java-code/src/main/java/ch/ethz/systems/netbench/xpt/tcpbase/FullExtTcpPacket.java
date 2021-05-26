package ch.ethz.systems.netbench.xpt.tcpbase;

import ch.ethz.systems.netbench.core.Simulator;
import ch.ethz.systems.netbench.ext.basic.TcpPacket;

import java.util.Collection;

public class FullExtTcpPacket extends TcpPacket implements SelectiveAckHeader, EchoHeader, PriorityHeader, Comparable {

    private double rateEst;
    private long priority;
    private long priorityRoot;
    private long flowSizeByte;
    private Collection<AckRange> selectiveAck;
    private long echoDepartureTime;
    private int echoFlowletId;
    private int enqueuedRound;
    private long enqueueTime;

    public FullExtTcpPacket(long flowId, long dataSizeByte, int sourceId, int destinationId, int TTL, int sourcePort, int destinationPort, long sequenceNumber, long acknowledgementNumber, boolean NS, boolean CWR, boolean ECE, boolean URG, boolean ACK, boolean PSH, boolean RST, boolean SYN, boolean FIN, double windowSize, long priority) {
        super(flowId, dataSizeByte, sourceId, destinationId, TTL, sourcePort, destinationPort, sequenceNumber, acknowledgementNumber, NS, CWR, ECE, URG, ACK, PSH, RST, SYN, FIN, windowSize);
        this.priority = priority;
        this.priorityRoot = priority;
        this.flowSizeByte = -1;
    }

    public FullExtTcpPacket(long flowId, long dataSizeByte, int sourceId, int destinationId, int TTL, int sourcePort, int destinationPort, long sequenceNumber, long acknowledgementNumber, boolean NS, boolean CWR, boolean ECE, boolean URG, boolean ACK, boolean PSH, boolean RST, boolean SYN, boolean FIN, double windowSize, long priority, long flowSizeByte) {
        super(flowId, dataSizeByte, sourceId, destinationId, TTL, sourcePort, destinationPort, sequenceNumber, acknowledgementNumber, NS, CWR, ECE, URG, ACK, PSH, RST, SYN, FIN, windowSize);
        this.priority = priority;
        this.priorityRoot = priority;
        this.flowSizeByte = flowSizeByte;
    }

    @Override
    public TcpPacket setEchoDepartureTime(long echoDepartureTime) {
        this.echoDepartureTime = echoDepartureTime;
        return this;
    }

    @Override
    public long getEchoDepartureTime() {
        return echoDepartureTime;
    }

    @Override
    public TcpPacket setEchoFlowletId(int echoFlowletId) {
        this.echoFlowletId = echoFlowletId;
        return this;
    }

    @Override
    public int getEchoFlowletId() {
        return echoFlowletId;
    }

    @Override
    public TcpPacket setSelectiveAck(Collection<AckRange> selectiveAck) {
        this.selectiveAck = selectiveAck;
        return this;
    }

    @Override
    public Collection<AckRange> getSelectiveAck() {
        return this.selectiveAck;
    }

    @Override
    public long getPriority() {
        return priority;
    }

    public long getRootPriority() {
        return priorityRoot;
    }

    @Override
    public void increasePriority() {
        priority++;
    }

    @Override
    public void setPriority(long val) {
        priority = val;
    }

    public void setRootPriority(long val) {
        priorityRoot = val;
    }

    @Override
    public int compareTo(Object o) {
        PriorityHeader header = (PriorityHeader) o;
        PriorityHeader header2 = (PriorityHeader) this;
        return Long.compare((int)header2.getPriority(), (int)header.getPriority());
    }

    public int getEnqueuedRound(){
        return enqueuedRound;
    }

    public long getEnqueueTime() { return enqueueTime; }

    public void setEnqueueTime(long enqueueTime) {this.enqueueTime = enqueueTime;}

    public void setEnqueuedRound(int enqueuedRound) {
        this.enqueuedRound = enqueuedRound;
    }


    public double getRateEst() {
        return this.rateEst;
    }


    public void setRateEst(double val) {
        this.rateEst = val;
    }

    public long getFlowSizeByte() { return this.flowSizeByte; }
}
