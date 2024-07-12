import pandas as pd
# import libsumo as traci
import traci
import numpy as np


def change_meter_rate(meter, meter_rate, green_duration = 2, control_step=0):
    """
    :param meter:
    :param meter_rate:
    :param green_duration:
    :param control_step:
    :return:
    """
    # retrieve ramp metering rate from the list
    rate = float(meter_rate.loc[control_step, meter])
    # calculate red duration based on green duration and ramp metering rate
    red_duration = ((1 - rate) * green_duration) / rate
    signal_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(meter)[0]
    for phase in signal_program.phases:
        if 'r' in phase.state:
            phase.duration = red_duration
    traci.trafficlight.setCompleteRedYellowGreenDefinition(meter, signal_program)
    print(signal_program)


def ALIANA_Controller(meter, r_pre, occu_down, occu_desire=20, K_R = 70, green_duration = 2, r_min = 400, r_max = 1800):
    r_k = r_pre + K_R * (occu_desire - occu_down)

    if r_k > r_max:
        r_k = r_max
    elif r_k < r_min:
        r_k = r_min

    red_duration = (3600 - r_k * green_duration) / r_k
    signal_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(meter)[0]
    for phase in signal_program.phases:
        if 'r' in phase.state:
            phase.duration = red_duration
    traci.trafficlight.setCompleteRedYellowGreenDefinition(meter, signal_program)
    print(signal_program)
    return r_k

def ALIANA_Controller_Initial(meter, green_duration = 2, r_k = 1800):
    red_duration = (3600 - r_k * green_duration) / r_k
    signal_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(meter)[0]
    for phase in signal_program.phases:
        if 'r' in phase.state:
            phase.duration = red_duration
    traci.trafficlight.setCompleteRedYellowGreenDefinition(meter, signal_program)
    return r_k

def ramp_close(meter):
    signal_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(meter)[0]
    for phase in signal_program.phases:
        if 'r' not in phase.state:
            print(phase.state)
            phase.duration = 0
    traci.trafficlight.setCompleteRedYellowGreenDefinition(meter, signal_program)


def ramp_open(meter):
    signal_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(meter)[0]
    for phase in signal_program.phases:
        if 'r' in phase.state:
            print(phase.state)
            phase.duration = 0
    traci.trafficlight.setCompleteRedYellowGreenDefinition(meter, signal_program)


def MeterRate_RandomGenerte(meter_list, total_step, min_rate=0.1, max_rate=1, max_diff=0.2):
    """
    :param meter_list: list of all ramp metering signal IDs
    :param total_step: total control step = total sim step/ control interval
    :param min_rate: the min allowed ramp metering rate
    :param max_rate: the maximum allowed ramp metering rate
    :param max_diff: the maximum allowed different of ramp metering rate between two consecutive control step
    :return: a pd data frame with all ramp metering rates
    """

    meter_rate_data = np.zeros((total_step, len(meter_list)))
    meter_rate_data[0] = np.random.uniform(min_rate, max_rate, size=len(meter_list))

    for i in range(1, total_step):
        for j in range(len(meter_list)):
            previous_value = meter_rate_data[i - 1, j]
            lower_bound = max(min_rate, previous_value - max_diff)
            upper_bound = min(max_rate, previous_value + max_diff)
            meter_rate_data[i, j] = np.random.uniform(lower_bound, upper_bound)

    # meter_rate_data = np.random.uniform(min_rate, max_rate, size=(total_step, len(meter_list)))
    meter_rate_data = np.round(meter_rate_data, decimals=2)
    meter_rate_random = pd.DataFrame(meter_rate_data, columns=meter_list)

    return meter_rate_random
