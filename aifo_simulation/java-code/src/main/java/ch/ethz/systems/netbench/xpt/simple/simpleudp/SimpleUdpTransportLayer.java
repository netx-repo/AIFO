package ch.ethz.systems.netbench.xpt.simple.simpleudp;

import ch.ethz.systems.netbench.core.network.Socket;
import ch.ethz.systems.netbench.core.network.TransportLayer;

public class SimpleUdpTransportLayer extends TransportLayer {

    SimpleUdpTransportLayer(int identifier) {
        super(identifier);
        this.udpException = true;
    }

    @Override
    protected Socket createSocket(long flowId, int destinationId, long flowSizeByte) {
        return new SimpleUdpSocket(this, flowId, identifier, destinationId, flowSizeByte, 80, 80);
    }

    @Override
    protected Socket createSocketWithRealFlowSize(long flowId, int destinationId, long flowSizeByte, long realFlowSizeByte) {
        if (flowSizeByte == -1) {
            return new SimpleUdpSocket(this, flowId, destinationId, identifier, flowSizeByte, realFlowSizeByte, 80, 80);
        }
        else {
            return new SimpleUdpSocket(this, flowId, identifier, destinationId, flowSizeByte, realFlowSizeByte, 80, 80);
        }
    }

    @Override
    protected Socket createSocketWithPort(long flowId, int destinationId, long flowSizeByte, int sourcePort, int destinationPort) {
        return new SimpleUdpSocket(this, flowId, identifier, destinationId, flowSizeByte, sourcePort, destinationPort);
    }

    @Override
    protected Socket createSocketWithPortAndRealFlowSize(long flowId, int destinationId, long flowSizeByte, long realFlowSizeByte, int sourcePort, int destinationPort) {
        if (flowSizeByte == -1) {
            return new SimpleUdpSocket(this, flowId, destinationId, identifier, flowSizeByte, realFlowSizeByte, sourcePort, destinationPort);
        }
        else {
            return new SimpleUdpSocket(this, flowId, identifier, destinationId, flowSizeByte, realFlowSizeByte, sourcePort, destinationPort);
        }
    }

}
