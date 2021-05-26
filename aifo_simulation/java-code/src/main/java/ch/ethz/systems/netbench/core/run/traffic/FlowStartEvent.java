package ch.ethz.systems.netbench.core.run.traffic;

import ch.ethz.systems.netbench.core.network.Event;
import ch.ethz.systems.netbench.core.network.TransportLayer;

public class FlowStartEvent extends Event {

    private final TransportLayer transportLayer;
    private final int targetId;
    private final long flowSizeByte;
    private long flowIdCounter;
    private boolean udpExp;
    private int sourcePort;
    private int destinationPort;
    /**
     * Create event which will happen the given amount of nanoseconds later.
     *
     * @param timeFromNowNs     Time it will take before happening from now in nanoseconds
     * @param transportLayer    Source transport layer that wants to send the flow to the target
     * @param targetId          Target network device identifier
     * @param flowSizeByte      Size of the flow to send in bytes
     */
    public FlowStartEvent(long timeFromNowNs, TransportLayer transportLayer, int targetId, long flowSizeByte) {
        super(timeFromNowNs);
        this.transportLayer = transportLayer;
        this.targetId = targetId;
        this.flowSizeByte = flowSizeByte;
        this.flowIdCounter = -1;
        this.udpExp = false;
        this.sourcePort = 80;
        this.destinationPort = 80;
    }

//    public FlowStartEvent(long timeFromNowNs, TransportLayer transportLayer, int targetId, long flowSizeByte, boolean udpExp) {
//        super(timeFromNowNs);
//        this.transportLayer = transportLayer;
//        this.targetId = targetId;
//        this.flowSizeByte = flowSizeByte;
//        this.flowIdCounter = -1;
//        this.udpExp = udpExp;
//    }
//
    public FlowStartEvent(long timeFromNowNs, TransportLayer transportLayer, int targetId, long flowSizeByte, long flowId) {
        super(timeFromNowNs);
        this.transportLayer = transportLayer;
        this.targetId = targetId;
        this.flowSizeByte = flowSizeByte;
        this.flowIdCounter = flowId;
        this.udpExp = false;
    }

    public FlowStartEvent(long timeFromNowNs, TransportLayer transportLayer, int targetId, long flowSizeByte, long flowId, boolean udpExp) {
        super(timeFromNowNs);
        this.transportLayer = transportLayer;
        this.targetId = targetId;
        this.flowSizeByte = flowSizeByte;
        this.flowIdCounter = flowId;
        this.udpExp = udpExp;
        this.sourcePort = 80;
        this.destinationPort = 80;
    }

    public FlowStartEvent(long timeFromNowNs, TransportLayer transportLayer, int targetId, long flowSizeByte, long flowId, int sourcePort, int destinationPort) {
        super(timeFromNowNs);
        this.transportLayer = transportLayer;
        this.targetId = targetId;
        this.flowSizeByte = flowSizeByte;
        this.flowIdCounter = flowId;
        this.udpExp = false;
        this.sourcePort = sourcePort;
        this.destinationPort = destinationPort;
    }

    public FlowStartEvent(long timeFromNowNs, TransportLayer transportLayer, int targetId, long flowSizeByte, long flowId, boolean udpExp, int sourcePort, int destinationPort) {
        super(timeFromNowNs);
        this.transportLayer = transportLayer;
        this.targetId = targetId;
        this.flowSizeByte = flowSizeByte;
        this.flowIdCounter = flowId;
        this.udpExp = udpExp;
        this.sourcePort = sourcePort;
        this.destinationPort = destinationPort;
    }

    @Override
    public void trigger() {
        if (this.flowIdCounter == -1) {
//            transportLayer.startFlow(targetId, flowSizeByte);
            transportLayer.startFlowWithPort(targetId, flowSizeByte, this.sourcePort, this.destinationPort);
        }
        else {
//            transportLayer.startFlowWithFlowId(targetId, flowSizeByte, flowIdCounter, this.udpExp);
            transportLayer.startFlowWithPortAndFlowId(targetId, flowSizeByte, flowIdCounter, this.udpExp, this.sourcePort, this.destinationPort);
        }
    }

}
