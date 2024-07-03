import os
from RUN_SIM import run_simulation, run_simulation_ramp_close, run_simulation_ramp_open
from XML2CSV import xml_to_csv


if __name__ == '__main__':
    run_simulation_ramp_open(total_sim_step=14400, control_interval=180, green_duation=5)
    #run_simulation_ramp_close(total_sim_step=14400, control_interval=180, green_duation=5)
    #run_simulation(total_sim_step=14400, control_interval=180, green_duation=5, min_rate=0.05, max_rate=0.3, warning=False)

    # Directory where all xml files are stored
    xml_dict = "Network_Files/Loop_Data_Ramp_Open/"
    file_list = os.listdir(xml_dict)

    # convert xml files to csv files
    for file in file_list:
        xml_file = os.path.join(xml_dict, file)
        xml_to_csv(xml_file, path='Sim_Results/Ramp_Open/')
