import os
import sys
import traci
import traci.constants as tc
import numpy as np
import pandas as pd
from RampMeter import ALIANA_Controller_Initial, change_meter_rate

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg"

def run_simulation_MPC(mpc_controller, total_sim_step = 7200, control_interval = 180,
                         warning = True, files_out_dict = "Loop_Data_Ramp_MPC/"):
    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

    total_control_step = int(total_sim_step / control_interval)

    meter_rate_table = pd.DataFrame(np.zeros((total_control_step, len(meter_list))), columns = meter_list)
    loop_detector_list = traci.inductionloop.getIDList()

    # create a list for all stations in the simulation (except "in" and "out")
    stations_list = []
    for loop in loop_detector_list:
        loop_parts = loop.split('_')
        station = f"{loop_parts[0]}_{loop_parts[1]}"
        stations_list.append(station)
    stations_list = set(stations_list)
    stations_list = sorted([item for item in stations_list if "in" not in item and "out" not in item])

    step = 0
    while step < total_sim_step:
        # at first step, set all ramp metering rates to 1800 veh/hr
        if step == 0:
            for meter in meter_list:
                r_k_meter = ALIANA_Controller_Initial(meter, r_k=1800)
                meter_rate_table.at[step / control_interval, meter] = r_k_meter
            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_NUMBER,))

        if step > 0 and step % control_interval == 0:
            # retrieve flow from loop detectors
            x0 = {station: 0 for station in stations_list}
            for station in stations_list:
                station_loops = [item for item in loop_detector_list if station in item]
                veh_number = 0
                for loop in station_loops:
                    veh_number += traci.inductionloop.getSubscriptionResults(loop)[tc.VAR_LAST_INTERVAL_NUMBER]
                x0[station] = veh_number
            x0 = np.array(list(x0.values())) * 3600/control_interval
            print(x0)

            if step / control_interval == 1:
                mpc_controller.x0 = x0
                mpc_controller.set_initial_guess()

            # call MPC controller
            print("calculating ramp metering rate using MPC controller")
            u0 = mpc_controller.make_step(x0)
            u0 = np.round(u0, 0)

            print("resetting ramp metering rate u0")
            for meter_num in range(len(meter_list)-3):
                meter = meter_list[meter_num+3]
                MPC_rate = u0[meter_num]
                change_meter_rate(meter=meter, rate = MPC_rate)
                meter_rate_table.at[step / control_interval, meter] = MPC_rate

            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_NUMBER,))

        traci.simulationStep()
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()
    meter_rate_table.to_csv('Results/Meter_Rate_MPC.csv', index=False)







