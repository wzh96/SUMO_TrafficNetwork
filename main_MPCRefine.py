import os
import pandas as pd
from run_simulation import run_simulation_MPC_Delayed
from XML2CSV import xml_to_csv
from utilis import params, MPC_params, setup_mpc
from MPC_Controller import Flow_Dynamics_Model, MPC_Controller
from SINDy import SINDy_Dynamics
from Data_Cleaner import data_loader_main

total_sim_step = params['total_sim_step']
control_interval = params['control_interval']

flow_all, _, occupancy_all, flow_dt, _, occupancy_dt = data_loader_main(csv_dict='Sim_Results/Ramp_MPC')

# import ramp metering data
control_input = pd.read_csv('Results/Meter_Rate_MPC.csv')

control_input = control_input/10
control_input = control_input.iloc[1:,:]

# obtain ODE equations
equations = SINDy_Dynamics(x = occupancy_all, dx = occupancy_dt, u = control_input, threshold = 0.0005)

# configure dynamics model
model = Flow_Dynamics_Model(equations)

# configure the MPC Controller
mpc = MPC_Controller(model=model, params=MPC_params, setup_mpc=setup_mpc, silence_solver=False)

run_simulation_MPC_Delayed(mpc_controller= mpc, total_sim_step=total_sim_step, control_interval=control_interval,
                   files_out_dict="Loop_Data_Ramp_MPCRefine/", sumoBinary="sumo", meter_rate_dict="Results/Meter_Rate_MPCRefine.csv")

# Directory where all xml files are stored
xml_dict = "Network_Files_2/Loop_Data_Ramp_MPCRefine/"
file_list = [file for file in os.listdir(xml_dict) if file.endswith('.xml')]
# convert xml files to csv files
for file in file_list:
    xml_file = os.path.join(xml_dict, file)
    xml_to_csv(xml_file, path='Sim_Results/Ramp_MPCRefine/')