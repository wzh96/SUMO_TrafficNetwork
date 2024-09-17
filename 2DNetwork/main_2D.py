import os
from run_simulation import (run_simulation_random, run_simulation_ramp_close,
                            run_simulation_ramp_open, run_simulation_ALIANA,
                            run_simulation_PIALINEA, run_simulation_FLALINEA)
from XML2CSV import xml_to_csv
from utilis_2D import params, ALINEA_params, MPC_params

if __name__ == '__main__':
    total_sim_step = params['total_sim_step']
    control_interval = params['control_interval']

    # run_scenarios = "No Control"
    # run_scenarios = "ALIANA"
    # run_scenarios = "PI-ALINEA"
    run_scenarios = "FL-ALINEA"
    # run_scenarios = "Random"

    if run_scenarios == "No Control":
        run_simulation_ramp_open(sumoBinary= "sumo", total_sim_step=total_sim_step, control_interval=control_interval, cfg_dict = "Network_Files_3/Traffic_Net.sumo.cfg")

        # Directory where all xml files are stored
        xml_dict = "Network_Files_3/Loop_Data_Ramp_Open/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_Open/')
    elif run_scenarios == "ALIANA":
        run_simulation_ALIANA(sumoBinary= "sumo", total_sim_step=total_sim_step, ALINEA_params=ALINEA_params, cfg_dict = "Network_Files_3/Traffic_Net.sumo.cfg",
                              control_interval=control_interval, meter_rate_dict = "Results/Meter_Rate_ALIANA.csv")

        # Directory where all xml files are stored
        xml_dict = "Network_Files_3/Loop_Data_Ramp_ALIANA/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_ALIANA/')


    elif run_scenarios == "PI-ALINEA":
        run_simulation_PIALINEA(sumoBinary="sumo-gui", total_sim_step=total_sim_step, ALINEA_params=ALINEA_params,
                              cfg_dict="Network_Files_3/Traffic_Net.sumo.cfg",
                              control_interval=control_interval, meter_rate_dict="Results/Meter_Rate_PIALINEA.csv")

        # Directory where all xml files are stored
        xml_dict = "Network_Files_3/Loop_Data_Ramp_PIALINEA/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_PIALINEA/')

    elif run_scenarios == "FL-ALINEA":
        run_simulation_FLALINEA(sumoBinary="sumo-gui", total_sim_step=total_sim_step, ALINEA_params=ALINEA_params,
                              cfg_dict="Network_Files_3/Traffic_Net.sumo.cfg",
                              control_interval=control_interval, meter_rate_dict="Results/Meter_Rate_FLALINEA.csv")

        # Directory where all xml files are stored
        xml_dict = "Network_Files_3/Loop_Data_Ramp_FLALINEA/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_FLALINEA/')

    elif run_scenarios == "Random":
        run_simulation_random(sumoBinary="sumo", total_sim_step=total_sim_step, cfg_dict = "Network_Files_3/Traffic_Net.sumo.cfg",
                              control_interval=control_interval, meter_rate_dict="Results/Meter_Rate_Random.csv")

        # Directory where all xml files are stored
        xml_dict = "Network_Files_3/Loop_Data_Ramp_Random/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_Random/')
