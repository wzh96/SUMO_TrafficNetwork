import os
from RUN_SIM_MPC import run_simulation_MPC
from XML2CSV import xml_to_csv
from utilis import params
from MPC_Controller import Flow_Dynamics_Model, MPC_Controller
from SINDy import SINDy_Dynamics
from Data_Cleaner import data_loader_main
import pandas as pd
from utilis import MPC_params, setup_mpc

total_sim_step = params['total_sim_step']
control_interval = params['control_interval']

flow_all, _, _, flow_dt, _, _ = data_loader_main(csv_dict='Sim_Results/Ramp_ALIANA')

# import ramp metering data
control_input = pd.read_csv('Results/Meter_Rate_ALIANA.csv')

control_input = control_input.iloc[:, 3:]

# obtain ODE equations
equations = SINDy_Dynamics(x = flow_all, dx = flow_dt, u = control_input)

# configure dynamics model
model = Flow_Dynamics_Model(equations)

# configure the MPC Controller
mpc = MPC_Controller(model, params=MPC_params, setup_mpc=setup_mpc, silence_solver=False)

run_simulation_MPC(mpc_controller= mpc, total_sim_step=total_sim_step, control_interval=control_interval)

# Directory where all xml files are stored
xml_dict = "Network_Files_2/Loop_Data_Ramp_MPC/"
file_list = os.listdir(xml_dict)
# convert xml files to csv files
for file in file_list:
    xml_file = os.path.join(xml_dict, file)
    xml_to_csv(xml_file, path='Sim_Results/Ramp_MPC/')