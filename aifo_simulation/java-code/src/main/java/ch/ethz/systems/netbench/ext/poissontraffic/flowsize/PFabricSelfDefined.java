package ch.ethz.systems.netbench.ext.poissontraffic.flowsize;

import ch.ethz.systems.netbench.core.log.SimulationLogger;

/**
 * pFabric (Alizadeh, 2016) data mining flow size distribution.
 *
 * Size (byte)  Idx         Culc. prob.
 0 1 0
 1000 1 0.500000
 2000 1 0.600000
 3000 1 0.700000
 5000 1 0.750000
 7000 1 0.800000
 40000 1 0.812500
 72000 1 0.825000
 137000 1 0.850000
 267000 1 0.900000
 1187000 1 0.95000
 2107000 1 1.0
 *
 * Expected flow size (upper bound):
 * 0.5*1000 + 0.1*2000 + 0.1*3000 + 0.05*5000 + 0.05*7000 + 0.0125*40000 + 0.0125*72000 + 0.025*137000 + 0.05*267000 + 0.05*1187000 +0.05*2107000
 * =
 * 184475 bytes
 * At 10 Gbps would take 18.6ms
*/
public class PFabricSelfDefined extends FlowSizeDistribution {

    public PFabricSelfDefined() {
        super();
        SimulationLogger.logInfo("Flow planner flow size dist.", "pFabric self defined discrete");
    }

    @Override
    public long generateFlowSizeByte() {

        double outcome = independentRng.nextDouble();

        if (outcome >= 0.0 && outcome <= 0.5) {
            return 1000;
        } else if (outcome >= 0.5 && outcome <= 0.6) {
            return 2000;
        } else if (outcome >= 0.6 && outcome <= 0.7) {
            return 3000;
        } else if (outcome >= 0.7 && outcome <= 0.75) {
            return 5000;
        } else if (outcome >= 0.75 && outcome <= 0.8) {
            return 7000;
        } else if (outcome >= 0.8 && outcome <= 0.8125) {
            return 40000;
        } else if (outcome >= 0.8125 && outcome <= 0.825) {
            return 72000;
        } else if (outcome >= 0.825 && outcome <= 0.85) {
            return 137000;
        } else if (outcome >= 0.85 && outcome <= 0.9) {
            return 267000;
        } else if (outcome >= 0.9 && outcome <= 0.95) {
            return 1187000;
        } else {
            return 2107000;
        }
    }
}
