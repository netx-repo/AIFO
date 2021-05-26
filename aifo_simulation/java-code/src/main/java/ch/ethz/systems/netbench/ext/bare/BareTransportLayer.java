package ch.ethz.systems.netbench.ext.bare;

import ch.ethz.systems.netbench.core.network.Socket;
import ch.ethz.systems.netbench.core.network.TransportLayer;
import ch.ethz.systems.netbench.ext.demo.DemoSocket;
import ch.ethz.systems.netbench.xpt.simple.simpleudp.SimpleUdpSocket;

public class BareTransportLayer extends TransportLayer {

    BareTransportLayer(int identifier) {
        super(identifier);
    }

    @Override
    protected Socket createSocket(long flowId, int destinationId, long flowSizeByte) {
        return new BareSocket(this, flowId, identifier, destinationId, flowSizeByte);
    }

    @java.lang.Override
    protected Socket createSocketWithRealFlowSize(long flowId, int destinationId, long flowSizeByte, long realFlowSizeByte) {
        return null;
    }

    @Override
    protected Socket createSocketWithPort(long flowId, int destinationId, long flowSizeByte, int sourcePort, int destinationPort) {
        return new BareSocket(this, flowId, identifier, destinationId, flowSizeByte);
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
