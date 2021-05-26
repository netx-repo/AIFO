package ch.ethz.systems.netbench.xpt.simple.simpleudp;


import ch.ethz.systems.netbench.core.log.SimulationLogger;
import ch.ethz.systems.netbench.core.network.TransportLayer;
import ch.ethz.systems.netbench.core.run.infrastructure.TransportLayerGenerator;

public class SimpleUdpTransportLayerGenerator extends TransportLayerGenerator {

    public SimpleUdpTransportLayerGenerator() {
        SimulationLogger.logInfo("Transport layer", "UDP");
    }

    @Override
    public TransportLayer generate(int identifier) {
        return new SimpleUdpTransportLayer(identifier);
    }
}
