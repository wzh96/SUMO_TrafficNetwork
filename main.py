import os
from RUN_SIM import run_simulation_random, run_simulation_ramp_close, run_simulation_ramp_open, run_simulation_ALIANA
from XML2CSV import xml_to_csv
from utilis import params

if __name__ == '__main__':
    total_sim_step = params['total_sim_step']
    control_interval = params['control_interval']

    run_scenarios = "No Control"
    # run_scenarios = "ALIANA"

    if run_scenarios == "No Control":
        run_simulation_ramp_open(sumoBinary= "sumo", total_sim_step=total_sim_step, control_interval=control_interval)

        # Directory where all xml files are stored
        xml_dict = "Network_Files_2/Loop_Data_Ramp_Open/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_Open/')
    elif run_scenarios == "ALIANA":
        run_simulation_ALIANA(sumoBinary= "sumo", total_sim_step=total_sim_step, control_interval=control_interval)

        # Directory where all xml files are stored
        xml_dict = "Network_Files_2/Loop_Data_Ramp_ALIANA/"
        file_list = os.listdir(xml_dict)

        # convert xml files to csv files
        for file in file_list:
            xml_file = os.path.join(xml_dict, file)
            xml_to_csv(xml_file, path='Sim_Results/Ramp_ALIANA/')
