package ch.ethz.systems.netbench.core.network;

import ch.ethz.systems.netbench.core.log.SimulationLogger;
import ch.ethz.systems.netbench.xpt.tcpbase.FullExtTcpPacket;

public class UDPSendPacketEvent extends Event {
    private final Socket udpsocket;
    public UDPSendPacketEvent(long timeFromNowNS, Socket udpsocket) {
        super(timeFromNowNS);
        this.udpsocket = udpsocket;
    }
    @java.lang.Override
    public void trigger() {
        this.udpsocket.start();
    }
}
