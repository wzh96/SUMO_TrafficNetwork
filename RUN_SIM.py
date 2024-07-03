import os
import sys
from RampMeter import MeterRate_RandomGenerte, change_meter_rate, ramp_close, ramp_open
import traci
#import libsumo as traci
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

def run_simulation(total_sim_step = 7200, control_interval = 180, green_duation = 5, min_rate = 0.1, max_rate = 1, warning = True, files_out_dict = "Loop_Data_Ramp_Random/"):
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
        sumoCmd = [sumoBinary, "-c", "Network_Files/Traffic_Net.sumo.cfg", "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", "Network_Files/Traffic_Net.sumo.cfg", "--output-prefix", files_out_dict]

    traci.start(sumoCmd)

    # get a list of all ramp metering signal ID
    meter_list = traci.trafficlight.getIDList()
    meter_list = sorted(meter_list)

    total_control_step = int(total_sim_step / control_interval)
    meter_rate = MeterRate_RandomGenerte(meter_list=meter_list, total_step=total_control_step, min_rate=min_rate, max_rate=max_rate)

    step = 0
    while step < total_sim_step:
        traci.simulationStep()
        # change
        if step % control_interval == 0:
            print("resetting ramp metering rate")
            for meter in meter_list:
                print(meter)
                change_meter_rate(meter=meter, meter_rate=meter_rate, green_duration=green_duation,
                                  control_step=step / control_interval)
        step += 1
        print("Simulation Step:" + str(step))

    traci.close()

    meter_rate.to_csv('Results/Meter_Rate.csv', index=False)


def run_simulation_ramp_close(total_sim_step = 7200, control_interval = 180, green_duation = 5, warning = True, files_out_dict = "Loop_Data_Ramp_Close/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :return:
    """
    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", "Network_Files/Traffic_Net.sumo.cfg", "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", "Network_Files/Traffic_Net.sumo.cfg", "--output-prefix", files_out_dict]

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


def run_simulation_ramp_open(total_sim_step = 7200, control_interval = 180, green_duation = 5, warning = True, files_out_dict = "Loop_Data_Ramp_Open/"):
    """
    :param total_sim_step:
    :param control_interval: ramp metering control step
    :param green_duation:
    :return:
    """
    sumoBinary = "sumo-gui"
    if warning:
        sumoCmd = [sumoBinary, "-c", "Network_Files/Traffic_Net.sumo.cfg", "--output-prefix", files_out_dict]
    else:
        sumoCmd = [sumoBinary, "--no-warnings", "-c", "Network_Files/Traffic_Net.sumo.cfg", "--output-prefix", files_out_dict]

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
