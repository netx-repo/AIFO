package ch.ethz.systems.netbench.xpt.aifo.ports.TailDrop;

import ch.ethz.systems.netbench.core.log.SimulationLogger;
import ch.ethz.systems.netbench.core.network.Link;
import ch.ethz.systems.netbench.core.network.NetworkDevice;
import ch.ethz.systems.netbench.core.network.OutputPort;
import ch.ethz.systems.netbench.core.network.Packet;
import ch.ethz.systems.netbench.ext.basic.IpHeader;
import ch.ethz.systems.netbench.xpt.tcpbase.FullExtTcpPacket;

import java.util.Arrays;
import java.util.concurrent.LinkedBlockingQueue;

public class TailDropOutputPort extends OutputPort {

    private final long maxQueueSizeBits;
    private int id,tid;
    TailDropOutputPort(NetworkDevice ownNetworkDevice, NetworkDevice targetNetworkDevice, Link link, long maxQueueSizeBytes) {
        super(ownNetworkDevice, targetNetworkDevice, link, new LinkedBlockingQueue<Packet>());
        this.maxQueueSizeBits = maxQueueSizeBytes * 8L;
        this.id = ownNetworkDevice.getIdentifier();
        this.tid = targetNetworkDevice.getIdentifier();
    }

    /**
     * Enqueue the given packet.
     * Drops it if the queue is full (tail drop).
     *
     * @param packet    Packet instance
     */
    @Override
    public void enqueue(Packet packet) {

        // Convert to IP packet
        IpHeader ipHeader = (IpHeader) packet;

        // Tail-drop enqueue
        
        if (this.queue.size() + 1 <= maxQueueSizeBits / 8 / 1460) {
            // Check whether there is an inversion for the packet enqueued
            if (SimulationLogger.hasInversionsTrackingEnabled()) {

                // Extract the packet rank
                FullExtTcpPacket p = (FullExtTcpPacket) packet;
                //System.out.println(p.getPriority());

                // We compute the perceived rank
                Object[] contentPIFO = super.getQueue().toArray();
                if (contentPIFO.length > 0){
                    Arrays.sort(contentPIFO);
                    FullExtTcpPacket packet_maxrank = (FullExtTcpPacket) contentPIFO[contentPIFO.length-1];
                    int rank_perceived = (int)packet_maxrank.getPriority();
                    //System.out.println(rank_perceived +"-----"+p.getPriority());
                    // We measure the inversion
                    if (rank_perceived > p.getPriority()){
                        SimulationLogger.logInversionsPerRank(this.getOwnId(), (int) p.getPriority(), 1);
                    }
                }
            }
            
            guaranteedEnqueue(packet);
        } else {
            SimulationLogger.increaseStatisticCounter("PACKETS_DROPPED");
            if (ipHeader.getSourceId() == this.getOwnId()) {
                SimulationLogger.increaseStatisticCounter("PACKETS_DROPPED_AT_SOURCE");
            }
        }

    }
}
