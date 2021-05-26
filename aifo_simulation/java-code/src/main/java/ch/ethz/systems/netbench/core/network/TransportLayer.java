package ch.ethz.systems.netbench.core.network;

import ch.ethz.systems.netbench.ext.basic.IpPacket;
import ch.ethz.systems.netbench.xpt.tcpbase.FullExtTcpPacket;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * The transport layer represents the entity that communicates
 * over the network. It belongs to a single {@link NetworkDevice network device}.
 * It starts a new {@link Socket socket} for each flow originating from here,
 * and creates a new receiving socket for each packet it receives with
 * an unfamiliar flow identifier.
 *
 * @see NetworkDevice
 * @see Socket
 */
public abstract class TransportLayer {

    // Generator for unique flow identifiers amongst all transport layers
    private static long flowIdCounter = 0;
    public boolean udpException = false;
    private static Map<Long, TransportLayer> flowIdToReceiver = new HashMap<>();

    // Map the flow identifier to the responsible socket
    private Map<Long, Socket> flowIdToSocket;
    private Set<Long> finishedFlowIds;

    // Map priority carried by data packets to flow identifier. Purpose: so that the same priority can
    // be applied to ACK packets as well. Only works for those cases in which priorities are fixed throughout all packets
    // of the flow.
    private Map<Long, Long> flowIdToPriority;

    private NetworkDevice networkDevice;
    protected final int identifier;

    public TransportLayer(int identifier) {
        this.identifier = identifier;
        this.flowIdToSocket = new HashMap<>();
        this.finishedFlowIds = new HashSet<>();
        this.flowIdToPriority = new HashMap<>();
    }

    /**
     * Pass the packet to the network device.
     *
     * @param packet    Packet instance
     */
    public final void send(Packet packet) {
        networkDevice.receiveFromTransportLayer(packet);
    }

    /**
     * Set the associated network device.
     *
     * Is not part of constructor because both the network device
     * and the server require a reference to each other.
     *
     * @param networkDevice     Network device instance
     */
    public final void setNetworkDevice(NetworkDevice networkDevice) {
        this.networkDevice = networkDevice;
    }

    /**
     * Reception of a packet from its network device (through the intermediary).
     * // TODO: make it package-local?
     *
     * @param genericPacket    Packet instance
     */
    public void receive(Packet genericPacket) {

        IpPacket packet = (IpPacket) genericPacket;
        FullExtTcpPacket fetPacket = (FullExtTcpPacket) genericPacket;
        Socket socket = flowIdToSocket.get(packet.getFlowId());
        // If the socket does not yet exist, it is an incoming socket
        if (socket == null && !finishedFlowIds.contains(packet.getFlowId())) {

            // Create the socket instance in the other direction
            if (fetPacket.getFlowSizeByte() == -1) {
//                socket = createSocket(packet.getFlowId(), packet.getSourceId(), -1);
                socket = createSocketWithPort(packet.getFlowId(), packet.getSourceId(), -1, fetPacket.getSourcePort(), fetPacket.getDestinationPort());
            }
            else {
                socket = createSocketWithPortAndRealFlowSize(packet.getFlowId(), packet.getSourceId(), -1, fetPacket.getFlowSizeByte(), fetPacket.getSourcePort(), fetPacket.getDestinationPort());
            }
            flowIdToReceiver.put(packet.getFlowId(), this);
            flowIdToSocket.put(packet.getFlowId(), socket);
        }

        // Give packet to socket (we do not care about stray packets)
        if (socket != null) {
            socket.handle(packet);
        }

    }

    /**
     * Start the sending of a flow to the destination.
     *
     * @param destination       Destination network device identifier
     * @param flowSizeByte      Byte size of the flow
     */
    public void startFlow(int destination, long flowSizeByte) {

        // Create new outgoing socket

//        Socket socket = createSocket(flowIdCounter, destination, flowSizeByte);
        Socket socket;
        if (this.udpException == true) {
            socket = createSocketWithRealFlowSize(flowIdCounter, destination, flowSizeByte, flowSizeByte);
        }
        else {
            socket = createSocket(flowIdCounter, destination, flowSizeByte);
        }
        flowIdToSocket.put(flowIdCounter, socket);
        flowIdCounter++;

        // Start the socket off as initiator
        socket.markAsSender();
        socket.start();

    }

    public void startFlowWithFlowId(int destination, long flowSizeByte, long flowId, boolean udpExp) {

        // Create new outgoing socket

//        Socket socket = createSocket(flowId, destination, flowSizeByte);
        Socket socket;
        if (udpExp == true) {
            socket = createSocketWithRealFlowSize(flowId, destination, flowSizeByte, flowSizeByte);
        }
        else {
            socket = createSocket(flowId, destination, flowSizeByte);
        }
        flowIdToSocket.put(flowId, socket);


        // Start the socket off as initiator
        socket.markAsSender();
        socket.start();

    }

    public void startFlowWithPort(int destination, long flowSizeByte, int sourcePort, int destinationPort) {

        // Create new outgoing socket

//        Socket socket = createSocket(flowIdCounter, destination, flowSizeByte);
        Socket socket;
        if (this.udpException == true) {
            socket = createSocketWithPortAndRealFlowSize(flowIdCounter, destination, flowSizeByte, flowSizeByte, sourcePort, destinationPort);
        }
        else {
            socket = createSocketWithPort(flowIdCounter, destination, flowSizeByte, sourcePort, destinationPort);
        }
        flowIdToSocket.put(flowIdCounter, socket);
        flowIdCounter++;

        // Start the socket off as initiator
        socket.markAsSender();
        socket.start();

    }

    public void startFlowWithPortAndFlowId(int destination, long flowSizeByte, long flowId, boolean udpExp, int sourcePort, int destinationPort) {

        // Create new outgoing socket

//        Socket socket = createSocket(flowId, destination, flowSizeByte);
        Socket socket;
        if (udpExp == true) {
            socket = createSocketWithPortAndRealFlowSize(flowId, destination, flowSizeByte, flowSizeByte, sourcePort, destinationPort);
        }
        else {
            socket = createSocketWithPort(flowId, destination, flowSizeByte, sourcePort, destinationPort);
        }
        flowIdToSocket.put(flowId, socket);


        // Start the socket off as initiator
        socket.markAsSender();
        socket.start();

    }
    /**
     * Create a socket instance
     * .
     * The created socket should assume it is a receiver, unless their
     * {@link Socket#start() start} method has been called.
     *
     * @param flowId            Flow identifier of the socket
     * @param destinationId     Destination network device identifier
     * @param flowSizeByte      Flow size to be transferred from source to destination in bytes
     *
     * @return  Socket instance
     */
    protected abstract Socket createSocket(long flowId, int destinationId, long flowSizeByte);
    protected abstract Socket createSocketWithRealFlowSize(long flowId, int destinationId, long flowSizeByte, long realFlowSizeByte);
    protected abstract Socket createSocketWithPort(long flowId, int destinationId, long flowSizeByte, int sourcePort, int destinationPort);
    protected abstract Socket createSocketWithPortAndRealFlowSize(long flowId, int destinationId, long flowSizeByte, long realFlowSizeByte, int sourcePort, int destinationPort);
    /**
     * Remove the socket from the transport layer after the flow has been finished.
     *
     * @param flowId    Flow identifier
     */
    private void removeSocket(long flowId) {
        this.finishedFlowIds.add(flowId);
        this.flowIdToSocket.remove(flowId);
    }

    public long getFlowPriority(long flowId){
        return this.flowIdToPriority.get(flowId);
    }

    /**
     * Clean up the socket references of a specific flow identifier (also overreaches
     * to the receiver).
     *
     * @param flowId    Flow identifier
     */
    void cleanupSockets(long flowId) {
        this.removeSocket(flowId);
        flowIdToReceiver.get(flowId).removeSocket(flowId);
    }

    /**
     * Reset the static run state.
     */
    public static void staticReset() {
//        flowIdCounter = 0;
        flowIdToReceiver.clear();
    }

//    public static void increaseFlowIdCounter() {
//        flowIdCounter += 30000;
//    }
}