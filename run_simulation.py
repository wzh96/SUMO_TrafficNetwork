import os
import sys
from RampMeter import MeterRate_RandomGenerte, change_meter_rate_random, ramp_close, ramp_open
from RampMeter import ALIANA_Controller_Initial, ALIANA_Controller, change_meter_rate
import traci
import traci.constants as tc
import numpy as np
import pandas as pd

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

# cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg"

def run_simulation_MPC(mpc_controller, total_sim_step = 7200, control_interval = 180,
                         warning = True, cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg", files_out_dict = "Loop_Data_Ramp_MPC/",
                       meter_rate_dict = "Results/Meter_Rate_MPC.csv", sumoBinary = "sumo-gui"):
    """

    :param mpc_controller:
    :param total_sim_step:
    :param control_interval:
    :param warning:
    :param files_out_dict:
    :return:
    """
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
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_NUMBER, tc.VAR_LAST_INTERVAL_OCCUPANCY))

        if step > 0 and step % control_interval == 0:
            # retrieve flow from loop detectors
            x0 = {station: 0 for station in stations_list}
            for station in stations_list:
                station_loops = [item for item in loop_detector_list if station in item]
                veh_number = 0
                total_occu = 0
                # for station loops collecting flow
                # for loop in station_loops:
                #     veh_number += traci.inductionloop.getSubscriptionResults(loop)[tc.VAR_LAST_INTERVAL_NUMBER]
                # x0[station] = veh_number

                # for station loops collecting occupancy
                for loop in station_loops:
                    total_occu += traci.inductionloop.getSubscriptionResults(loop)[tc.VAR_LAST_INTERVAL_OCCUPANCY]
                x0[station] = total_occu / len(station_loops)

            # x0 = np.array(list(x0.values())) * 3600/control_interval
            x0 = np.array(list(x0.values()))
            print(x0)

            if step / control_interval == 1:
                mpc_controller.x0 = x0
                mpc_controller.set_initial_guess()

            # call MPC controller
            print("calculating ramp metering rate using MPC controller")
            u0 = mpc_controller.make_step(x0)
            # u0 = np.round(u0, 0)
            u0 = np.round(u0 * 10, 0)

            print("resetting ramp metering rate u0")
            for meter_num in range(len(meter_list)):
                meter = meter_list[meter_num]
                MPC_rate = u0[meter_num]
                change_meter_rate(meter=meter, rate = MPC_rate)
                meter_rate_table.at[step / control_interval, meter] = MPC_rate

            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_NUMBER, tc.VAR_LAST_INTERVAL_OCCUPANCY))

        traci.simulationStep()
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()
    meter_rate_table.to_csv(meter_rate_dict, index=False)


def run_simulation_MPC_Delayed(mpc_controller, MPC_params, ALINEA_params, total_sim_step = 7200, burnin_step = 1800, control_interval = 180,
                         warning = True, cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg", files_out_dict = "Loop_Data_Ramp_MPC/",
                       meter_rate_dict = "Results/Meter_Rate_MPC.csv", sumoBinary = "sumo-gui"):
    """

    :param mpc_controller:
    :param total_sim_step:
    :param control_interval:
    :param warning:
    :param files_out_dict:
    :return:
    """
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
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_NUMBER, tc.VAR_LAST_INTERVAL_OCCUPANCY))

        # during burnin_step, apply ALINEA or (no control at all)
        if step > 0 and step <= burnin_step and step % control_interval == 0:
            print("resetting ramp metering rate using ALINEA")

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

                # Apply ALIANA control
                r_pre = meter_rate_table.at[(step / control_interval - 1), meter]
                r_k_meter = ALIANA_Controller(meter, r_pre=r_pre, occu_down=occu_down, occu_desire=ALINEA_params['desire_occu'],
                                              K_R=ALINEA_params['K_R'], r_min=ALINEA_params['r_min'], r_max=ALINEA_params['r_max'])
                meter_rate_table.at[step / control_interval, meter] = r_k_meter

            # reset loop detectors subscription list
            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (traci.constants.VAR_LAST_INTERVAL_OCCUPANCY,))


        if step > burnin_step and step % control_interval == 0:
            # retrieve flow from loop detectors
            x0 = {station: 0 for station in stations_list}
            for station in stations_list:
                station_loops = [item for item in loop_detector_list if station in item]
                veh_number = 0
                total_occu = 0
                # for station loops collecting flow
                # for loop in station_loops:
                #     veh_number += traci.inductionloop.getSubscriptionResults(loop)[tc.VAR_LAST_INTERVAL_NUMBER]
                # x0[station] = veh_number

                # for station loops collecting occupancy
                for loop in station_loops:
                    total_occu += traci.inductionloop.getSubscriptionResults(loop)[tc.VAR_LAST_INTERVAL_OCCUPANCY]
                x0[station] = total_occu / len(station_loops)

            x0 = np.array(list(x0.values()))
            print(x0)

            # apply MPC controller if any of the occupancy is great that the desired occupancy.
            if np.sum(x0 > MPC_params['desire_occu']) >= 0:
                # call MPC controller
                print("calculating ramp metering rate using MPC controller")
                u0 = mpc_controller.make_step(x0)
                # u0 = np.round(u0, 0)
                u0 = np.round(u0 * 10, 0)

                print("resetting ramp metering rate u0")
                for meter_num in range(len(meter_list)):
                    meter = meter_list[meter_num]
                    MPC_rate = u0[meter_num]
                    change_meter_rate(meter=meter, rate=MPC_rate)
                    meter_rate_table.at[step / control_interval, meter] = MPC_rate

            else:
                # if no occupancy is greater than the desired occupancy
                print("no ramp metering needed")
                for meter in meter_list:
                    print(meter)
                    r_k_meter = ALIANA_Controller_Initial(meter, r_k=1800)
                    meter_rate_table.at[step / control_interval, meter] = r_k_meter

            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (tc.VAR_LAST_INTERVAL_NUMBER, tc.VAR_LAST_INTERVAL_OCCUPANCY))

        traci.simulationStep()
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()
    meter_rate_table.to_csv(meter_rate_dict, index=False)


def run_simulation_ALIANA(ALINEA_params, sumoBinary = "sumo-gui", total_sim_step = 7200, control_interval = 180,
                          warning = True, cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg",
                          files_out_dict = "Loop_Data_Ramp_ALIANA/",
                          meter_rate_dict = "Results/Meter_Rate_ALIANA.csv",):

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
                r_k_meter = ALIANA_Controller(meter, r_pre=r_pre , occu_down=occu_down, occu_desire=ALINEA_params['desire_occu'],
                                              K_R=ALINEA_params['K_R'], r_min = ALINEA_params['r_min'], r_max = ALINEA_params['r_max'])
                meter_rate_table.at[step / control_interval, meter] = r_k_meter

            # reset loop detectors subscription list
            for loop in loop_detector_list:
                traci.inductionloop.subscribe(loop, (traci.constants.VAR_LAST_INTERVAL_OCCUPANCY, ))

        traci.simulationStep()
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()
    meter_rate_table.to_csv(meter_rate_dict, index=False)

def run_simulation_ramp_close(sumoBinary = "sumo-gui", total_sim_step = 7200, control_interval = 180, green_duation = 5, warning = True,
                              cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg", files_out_dict = "Loop_Data_Ramp_Close/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :return:
    """

    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    # get a list of all ramp metering signal ID
    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

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

def run_simulation_ramp_open(sumoBinary = "sumo-gui", total_sim_step = 7200, control_interval = 120, warning = True,
                             cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg", files_out_dict = "Loop_Data_Ramp_Open/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :return:
    """

    if warning:
        sumoCmd = [sumoBinary, "-c", cfg_dict, "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", cfg_dict, "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    # get a list of all ramp metering signal ID
    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

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


def run_simulation_random(sumoBinary = "sumo-gui", total_sim_step = 7200, control_interval = 180,
                          green_duration = 2, min_rate = 100, max_rate = 1800, warning = True, cfg_dict = "Network_Files_2/Traffic_Net.sumo.cfg",
                          files_out_dict ="Loop_Data_Ramp_Random/", meter_rate_dict = "Results/Meter_Rate_Random.csv"):
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
                change_meter_rate_random(meter=meter, meter_rate=meter_rate, green_duration=green_duration,
                                         control_step=step / control_interval)
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()

    meter_rate.to_csv(meter_rate_dict, index=False)