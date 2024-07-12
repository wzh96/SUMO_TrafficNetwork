import os
import sys
from RampMeter import MeterRate_RandomGenerte, change_meter_rate, ramp_close, ramp_open
from RampMeter import ALIANA_Controller_Initial, ALIANA_Controller
import traci
import traci.constants as tc
import numpy as np
import pandas as pd

#import libsumo as traci
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg"

def run_simulation(total_sim_step = 7200, control_interval = 180, green_duration = 5, min_rate = 0.1, max_rate = 1, warning = True, files_out_dict = "Loop_Data_Ramp_Random/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :param min_rate:
    :param max_rate:
    :param warning:
    :param files_out_dict:
    :return:
    """
    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    # get a list of all ramp metering signal ID
    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

    total_control_step = int(total_sim_step / control_interval)
    meter_rate = MeterRate_RandomGenerte(meter_list=meter_list, total_step=total_control_step, min_rate=min_rate, max_rate=max_rate)

    step = 0
    while step < total_sim_step:
        traci.simulationStep()
        # change ramp metering rate
        if step % control_interval == 0:
            print("resetting ramp metering rate")
            for meter in meter_list:
                print(meter)
                change_meter_rate(meter=meter, meter_rate=meter_rate, green_duration=green_duration,
                                  control_step=step / control_interval)
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()

    meter_rate.to_csv('Results/Meter_Rate.csv', index=False)

def run_simulation_ALIANA(total_sim_step = 7200, control_interval = 180, r_min = 100, r_max = 1800,
                          occu_desire=20, K_R = 50, warning = True, files_out_dict = "Loop_Data_Ramp_ALIANA/"):

    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

    total_control_step = int(total_sim_step / control_interval)

    # create a table to record meter rate for all meters
    meter_rate_table = pd.DataFrame(np.zeros((total_control_step, len(meter_list))), columns = meter_list)

    loop_detector_list = traci.inductionloop.getIDList()

    step = 0
    while step < total_sim_step:

        # set initial rate of all meters to 1800
        if step == 0:
            for meter in meter_list:
                r_k_meter = ALIANA_Controller_Initial(meter, r_k=1800)
                meter_rate_table.at[step / control_interval, meter] = r_k_meter

            # at the initial step, scribe loop detectors for occupancy values
            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_OCCUPANCY,))

        # change ramp metering rate
        if step > 0 and step % control_interval == 0:
            print("resetting ramp metering rate")

            # loop through each meter
            for meter in meter_list:
                print(meter)
                meter_parts = meter.split('_')
                station = f"{meter_parts[0]}_{meter_parts[2]}"
                downstream_loops = tuple(s for s in loop_detector_list if s.startswith(station))

                # retrieve downstream occupancy
                occus_down_station = {loop: None for loop in downstream_loops}
                for loop in downstream_loops:
                    occu_down_single = traci.inductionloop.getSubscriptionResults(loop)[tc.VAR_LAST_INTERVAL_OCCUPANCY]
                    occus_down_station[loop] = occu_down_single
                occu_down = sum(occus_down_station.values()) / len(occus_down_station)

                #Apply ALIANA control
                r_pre = meter_rate_table.at[(step/control_interval-1), meter]
                r_k_meter = ALIANA_Controller(meter, r_pre=r_pre , occu_down=occu_down, occu_desire=occu_desire, K_R=K_R, r_min = r_min, r_max = r_max)
                meter_rate_table.at[step / control_interval, meter] = r_k_meter

            # reset loop detectors subscription list
            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (traci.constants.VAR_LAST_INTERVAL_OCCUPANCY, traci.constants.VAR_LAST_INTERVAL_NUMBER))

        traci.simulationStep()
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()
    meter_rate_table.to_csv('Results/Meter_Rate.csv', index=False)

def run_simulation_ramp_close(total_sim_step = 7200, control_interval = 180, green_duation = 5, warning = True, files_out_dict = "Loop_Data_Ramp_Close/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :return:
    """
    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    # get a list of all ramp metering signal ID
    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

    total_control_step = int(total_sim_step / control_interval)
    #meter_rate = MeterRate_RandomGenerte(meter_list=meter_list, total_step=total_control_step, min_rate=0.1, max_rate=1)

    step = 0
    while step < total_sim_step:
        traci.simulationStep()
        # change
        if step % control_interval == 0:
            print("resetting ramp metering rate")
            for meter in meter_list:
                print(meter)
                ramp_close(meter)
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()


def run_simulation_ramp_open(total_sim_step = 7200, control_interval = 120, warning = True, files_out_dict = "Loop_Data_Ramp_Open/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :return:
    """
    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    # get a list of all ramp metering signal ID
    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

    total_control_step = int(total_sim_step / control_interval)
    #meter_rate = MeterRate_RandomGenerte(meter_list=meter_list, total_step=total_control_step, min_rate=0.1, max_rate=1)

    step = 0
    while step < total_sim_step:
        traci.simulationStep()
        # change
        if step % control_interval == 0:
            print("resetting ramp metering rate")
            for meter in meter_list:
                print(meter)
                ramp_open(meter)
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()
