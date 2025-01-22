import os
import pandas as pd
from run_simulation import run_simulation_MPC_Delayed
from XML2CSV import xml_to_csv
from utilis_2D import params, MPC_params, setup_mpc, ALINEA_params
from DMDMPC_Controller_2D import Flow_Dynamics_Model, MPC_Controller
from Data_Cleaner import data_loader_main
from SINDy import DMD_Dynamics
from pydmd import DMDc
import numpy as np
import casadi as ca

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


# occupancy_all, occupancy_dt = occupancy_all.iloc[:-1, :].reset_index(drop=True), occupancy_dt.iloc[:-1, :].reset_index(drop=True)
control_input = control_input.iloc[1:,:].reset_index(drop=True)

occupancy_all = np.array(occupancy_all)
control_input = np.array(control_input)

dmdc = DMDc(svd_rank=-1)
dmdc.fit(X=occupancy_all.T, I=control_input.T)

eigs = np.power(
            dmdc.eigs, dmdc.dmd_time["dt"] // dmdc.original_time["dt"]
        )

A = np.linalg.multi_dot(
            [dmdc.modes, np.diag(eigs), np.linalg.pinv(dmdc.modes)]
        )
A= A.real
B= dmdc.B

def create_equations(A, B):
    equations = []
    num_equations = A.shape[0]  # Number of equations (rows of A)
    num_states = A.shape[1]  # Number of states (columns of A)
    num_controls = B.shape[1]  # Number of controls (columns of B)

    for i in range(num_equations):
        terms = []
        # Add terms from matrix A
        for j in range(num_states):
            coeff = A[i, j]
            if coeff != 0:
                # Round the coefficient to 6 decimal places
                rounded_coeff = round(coeff, 6)
                terms.append(f"{rounded_coeff}*x{j}")
        # Add terms from matrix B
        for k in range(num_controls):
            coeff = B[i, k]
            if coeff != 0:
                # Round the coefficient to 6 decimal places
                rounded_coeff = round(coeff, 6)
                terms.append(f"{rounded_coeff}*u{k}")
        # Combine terms into an equation
        equation = " + ".join(terms)
        equations.append(equation)
    return equations
# Generate the equations
equations = create_equations(A, B)

model = Flow_Dynamics_Model(equations)
setup_mpc['n_horizon'] = 4

mpc = MPC_Controller(model=model, params=MPC_params, setup_mpc=setup_mpc, silence_solver=False)

run_simulation_MPC_Delayed(sumoBinary="sumo-gui", mpc_controller= mpc, total_sim_step=total_sim_step, control_interval=control_interval,
                           burnin_step = burnin_step, MPC_params= MPC_params, ALINEA_params= ALINEA_params,
                           cfg_dict = "Network_Files_3/Traffic_Net.sumo.cfg",
                           files_out_dict="Loop_Data_Ramp_DMDMPC/",
                           meter_rate_dict="Results/Meter_Rate_DMDMPC.csv")

# Directory where all xml files are stored
xml_dict = "Network_Files_3/Loop_Data_Ramp_DMDMPC/"
file_list = [file for file in os.listdir(xml_dict) if file.endswith('.xml')]
# convert xml files to csv files
for file in file_list:
    xml_file = os.path.join(xml_dict, file)
    xml_to_csv(xml_file, path='Sim_Results/Ramp_DMDMPC/')