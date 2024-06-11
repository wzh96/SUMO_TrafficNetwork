import os
import sys
import pandas as pd
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import libsumo as traci

sumoBinary = "sumo"
sumoCmd = [sumoBinary, "--no-warnings", "-c", "Network_Files/Traffic_Net.sumo.cfg"]

traci.start(sumoCmd)

# get a list of all induction loop detector in the network
det_list = traci.inductionloop_getIDList()

flow_all = pd.DataFrame()

step = 0
while step <= 3600:
    traci.simulationStep()
    flow_sum = {}
    for det in det_list:
        flow = traci.inductionloop_getIntervalVehicleNumber(det)
        flow_sum[det] = [flow]
    flow_sum = pd.DataFrame(flow_sum)
    flow_all = pd.concat([flow_all, flow_sum], ignore_index=True)
    step += 1

traci.close()
flow_all.to_csv("Sim_Results/Sim_Results.csv", index=True)
