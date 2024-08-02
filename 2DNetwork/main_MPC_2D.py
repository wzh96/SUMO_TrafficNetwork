import os
import pandas as pd
from run_simulation import run_simulation_MPC_Delayed
from XML2CSV import xml_to_csv
from utilis_2D import params, MPC_params, setup_mpc, ALINEA_params
from MPC_Controller_2D import Flow_Dynamics_Model, MPC_Controller
from SINDy import SINDy_Dynamics
from Data_Cleaner import data_loader_main

total_sim_step = params['total_sim_step']
control_interval = params['control_interval']
burnin_step = params['burnin_step']
burnin_control_step = int(burnin_step/control_interval) # calculate the control step that are within the burnin period

flow_all, _, occupancy_all, flow_dt, _, occupancy_dt = data_loader_main(csv_dict='Sim_Results/Ramp_ALIANA')

# import ramp metering data
control_input = pd.read_csv('Results/Meter_Rate_ALIANA.csv')
control_input = control_input/10

occupancy_all, occupancy_dt = occupancy_all.iloc[burnin_control_step:, :], occupancy_dt.iloc[burnin_control_step:, :]
control_input = control_input.iloc[burnin_control_step:, :]

occupancy_all, occupancy_dt = occupancy_all.iloc[:-1, :].reset_index(drop=True), occupancy_dt.iloc[:-1, :].reset_index(drop=True)
control_input = control_input.iloc[1:,:].reset_index(drop=True)

# obtain ODE equations
equations = SINDy_Dynamics(x = occupancy_all, dx = occupancy_dt, u = control_input, threshold = 0.0002)

# configure dynamics model
model = Flow_Dynamics_Model(equations)

# configure the MPC Controller
setup_mpc['n_horizon'] = 7
mpc = MPC_Controller(model=model, params=MPC_params, setup_mpc=setup_mpc, silence_solver=False)

# run_simulation_MPC_Delayed(sumoBinary="sumo", mpc_controller= mpc, total_sim_step=total_sim_step, control_interval=control_interval,
#                            burnin_step = burnin_step, MPC_params= MPC_params, ALINEA_params= ALINEA_params,
#                            cfg_dict = "Network_Files_3/Traffic_Net.sumo.cfg",
#                            files_out_dict="Loop_Data_Ramp_MPC/",
#                            meter_rate_dict="Results/Meter_Rate_MPC.csv")

# Directory where all xml files are stored
xml_dict = "Network_Files_3/Loop_Data_Ramp_MPC/"
file_list = [file for file in os.listdir(xml_dict) if file.endswith('.xml')]
# convert xml files to csv files
for file in file_list:
    xml_file = os.path.join(xml_dict, file)
    xml_to_csv(xml_file, path='Sim_Results/Ramp_MPC/')