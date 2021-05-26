
# AIFO: Analysis and performance evaluation (Simulation)

## Build and Run

#### 1. Software dependencies

* **Java 8:** Version 8 of Java; both Oracle JDK and OpenJDK are supported and produce under that same seed deterministic results. Additionally the project uses the **Apache Maven** software project management and comprehension tool (version 3+).

* **Python 3:** Recent version of Python 3 for analysis; be sure you can globally run `python3 <script.py>`. Packge required: pandas, matplotlib. You can install them via pip.

#### 2. Building

Build the executable `NetBench.jar` by using the following maven command: 
```
mvn clean compile assembly:single
```

#### 3. Running

1. Execute a demo run by using the following command: 
    ```
    java -jar -ea NetBench.jar x
    ``` 
   where `x` is the index of figure in the paper (i.e. 7, 8, 9, 10, 11, 12, 13, 16, or 0) (e.g., `java -jar -ea NetBench.jar 7` runs simulations for Figure 7). When `x` is 0, all experiments will be run sequentially. **Please do not open multiple terminals and run multiple figures concurrently, since the `temp` file paths can be overlapping**

2. After the run, the log files are saved in the `./temp/aifo/aifo_evaluation` folder

3. If you have python 3 installed, you can view calculated statistics about flow completion and port utilization (e.g. mean FCT, 99th %-tile port utilization, ....) in the `./temp/aifo/.../analysis` folder

4. Results after analysis are stored in the `./projects/aifo/plots` folder

5. We provide a script `../../parse.py` to generate the figures for all the results. Please check the usage [here](../../README.md).

#### 4. Example

Let's now go for an example, wanting to reproduce the experiments required to reproduce Figure 7: Simulation results of web search workload to minimize FCT.

1. Build the executable `NetBench.jar` by using the following maven command: `mvn clean compile assembly:single`

2. Execute those simulations by using the following command: `java -jar -ea NetBench.jar 7`. This command is to invoke the main method of `./src/main/java/ch.ethz.systems.netbench/core/run/MainFigure7.java`

3. Look into folder `temp/aifo/`, it contains the raw log files for each of the run simulations.

4. Look into folder `projects/aifo/plots/aifo_evaluation/pFabric/web_search_workload`, it contains the analysis of those log files and data for generating the plots. 

5. We provide a script `../../parse.py` to generate the figures for all the results. Please check the usage [here](../../README.md).

6. Feel free to modify the configuration files and repeat the process to see the effects of your changes to the final results.

#### 5. Running time

Figure 7, 8, and 11 take approximately 15 hours. Figure 10 and 13 take approximately 3 hours. Figure 12 and 16 take approximately 10 seconds. And Figure 9 takes approximately 35 hours. The actual running time depends on the machine you use.

## Software structure

There are three sub-packages in [*netbench*](https://github.com/nsg-ethz/sp-pifo): (a) core, containing core functionality, (b) ext (extension), which contains functionality implemented and quite thoroughly tested, and (c) xpt (experimental), which contains functionality not yet as thoroughly tested but reasonably vetted and assumed to be correct for the usecase it was written for.

The framework is written based on five core components:
1. **Network device**: abstraction of a node, can be a server (has a transport layer) or merely function as switch (no transport layer);
2. **Transport layer**: maintains the sockets for each of the flows that are started at the network device and for which it is the destination;
3. **Intermediary**: placed between the network device and transport layer, is able to modify each packet before arriving at the transport layer and after leaving the transport layer;
4. **Link**: quantifies the capabilities of the physical link, which the output port respects;
5. **Output port**: models output ports and their queueing behavior.

Look into `ch.ethz.systems.netbench.ext.demo` for an impression how to extend the framework.  If you've written an extension, it is necessary to add it in its respective selector in `ch.ethz.systems.netbench.run`. If you've added new properties, be sure to add them in the `ch.ethz.systems.netbench.config.BaseAllowedProperties` class.

More information about the framework can be found in the thesis located at [https://www.research-collection.ethz.ch/handle/20.500.11850/156350](https://www.research-collection.ethz.ch/handle/20.500.11850/156350) (section 4.2: NetBench: Discrete Packet Simulator).

---

## Remarks

#### General remarks about structure

1. Make sure you understand and ran through the Getting Started section above. 

2. AIFO files are placed within the `./projects/aifo` folder, which aims to be separated from the original [NetBench](https://github.com/ndal-eth/netbench) code for the sake of modularity.

* **Run configurations**:  All run configurations are placed in the `./projects/aifo/runs` folder, organized based on the Figures presented in the paper. Note that some configurations are overwritten in the `MainFigure_.java` files located in the `./src/main/java/ch/ethz/systems/netbench/core/run` folder

 * **Output simulations**: The output of the runs are written to the `./temp/aifo` folder.

 * **Result analysis**: The scripts used to analyze the simulation results, `analyze.py`, and to generate the paper plots, `plot.gnuplot`, are placed in the `./projects/sppifo/plots` folder, under the same organizational structure:

    * `./project/aifo/plots/aifo_evaluation/pFabric/web_search_workload` contains the results for Figure 7.
    * `./project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_C_K` contains the results for Figure 8.
    * `./project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_w_sr` contains the results for Figure 9. 
    * `./project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len_1_4` contains the results for Figure 10. 
    * `./project/aifo/plots/aifo_evaluation/pFabric/web_search_workload_q_len` contains the results for Figure 11.
    * `./projects/aifo/plots/aifo_evaluation/selfDefinedFlows` contains the results for Figure 12 and 16.
    * `./project/aifo/plots/aifo_evaluation/fairness/web_search_workload` contains the results for Figure 13.

 * **Main file to run the simulations**: The simulations can be executed by running the file `MainFigure_.java` file, located in `src/main/java/ch.ethz.systems.netbench/core/run`. Each file is responsible for (i) executing all the simulations as configured in `./projects/aifo/runs`,  (ii) generating the output results for those simulations in `./temp/aifo/`, and (iii) analyzing those results to generate the plots in `./projects/aifo/plots` for a single figure in our paper.

    * Pro tip: Just import the `pom.xml` file to your favorite SDK (we used [IntelliJ IDEA](https://www.jetbrains.com/idea/download/)), which provides all the configuration for the Maven project. 

#### Extensions to the original [NetBench](https://github.com/ndal-eth/netbench) and [SP-PIFO](https://github.com/nsg-ethz/sp-pifo)

We utilizes and extends SP-PIFO's extensions to the original NetBench simulator. Details about those extensions in the following lines. 

 * **Output ports and transport layers**: They can be found within the *xpt (experimental)* sub-package in the main source code of the simulator (i.e., `src.main.java.ch.ethz.systems.netbench.xpt`). In particular:

    * `xpt/aifo/ports` contains the implementations of the scheduling algorithms used on our simulations which were not available in the original distribution (e.g., FIFO, PIFO, AFQ, SP-PIFO, and AIFO).
    * `core/config/exceptions/BaseAllowedProperties` and `core/config/run/traffic/InfrastructureSelector` contain the configuration parameters which are required to use those output ports and transport layers. 

 * **Loggers**: We have added new loggers to track the arriving order at the receiver (Figure 12 and 16). 

    * `core/config/log/SimulationLogger` contains those extra loggers with their respective configurations. 
    * `core/SelfDefinedFlows` contains a boolean variable that is used to enable/disable the logger.
    * `ext/poissontraffic/PoissonArrivalPlanner` contains code for registering self-defined flows.
    * `core/network/OutputPort` contains code for enabling logging the arriving order.
