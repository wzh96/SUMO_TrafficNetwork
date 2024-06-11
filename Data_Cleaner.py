import pandas as pd
import numpy as np
import os

# Directory where all xml files are stored
xml_dict = "Network_Files/Loop_Data"
file_list = os.listdir(xml_dict)

station_list = [
    f"{parts[0]}_{parts[1]}" if len(parts) > 2 else os.path.splitext(f"{parts[0]}_{parts[1]}")[0]
    for parts in (file_name.split('_') for file_name in file_list)
]

station_list = list(set(station_list))

station_list = sorted(station_list)

# Stations (system in and system out)
station_inout_list = [stat for stat in station_list if "in" in stat or "out" in stat]

# Station (onRamp and offRamp)
station_ramp_list = [stat for stat in station_list if "onRamp" in stat or "offRamp" in stat]

# Station (Main Lane)
station_main_list = [stat for stat in station_list if stat not in station_inout_list and stat not in station_ramp_list]

# csv file directory:
csv_dict = "Sim_Results"

def data_loader_main():
    flow_all = pd.DataFrame()
    speed_all = pd.DataFrame()
    occupancy_all = pd.DataFrame()

    # loop through all stations in the station_list
    for station in station_main_list:
        station_file = {}
        for file in os.listdir(csv_dict):
            if station in file:
                station_file[file] = pd.read_csv(os.path.join(csv_dict, file))
        print(station + " file loaded successfully")
        station_file_merged = pd.concat(station_file.values(), axis=1)

        # summarize flow collected from detectors
        station_file_red = station_file_merged[['begin', 'end', 'id', 'flow', 'speed', 'occupancy']].copy()
        station_file_red.loc[:, 'flow_all'] = station_file_red[['flow']].sum(axis=1)
        station_file_red[['speed']] = station_file_red[['speed']].replace(-1, np.nan, inplace=False)
        station_file_red['speed_all'] = station_file_red[['speed']].mean(axis=1)
        station_file_red['occupancy_all'] = station_file_red[['occupancy']].mean(axis=1)

        station_flow = station_file_red[['flow_all']]
        station_speed = station_file_red[['speed_all']]
        station_occupancy = station_file_red[['occupancy_all']]

        station_flow.columns = [station]
        station_speed.columns = [station]
        station_occupancy.columns = [station]

        flow_all = pd.concat([flow_all, station_flow], axis=1)
        speed_all = pd.concat([speed_all, station_speed], axis=1)
        occupancy_all = pd.concat([occupancy_all, station_occupancy], axis=1)

    return flow_all, speed_all, occupancy_all

def data_loader_inout():
    flow_all = pd.DataFrame()
    speed_all = pd.DataFrame()
    occupancy_all = pd.DataFrame()

    # loop through all stations in the station_list
    for station in station_inout_list:
        station_file = {}
        for file in os.listdir(csv_dict):
            if station in file:
                station_file[file] = pd.read_csv(os.path.join(csv_dict, file))
        print(station + " file loaded successfully")
        station_file_merged = pd.concat(station_file.values(), axis=1)

        # summarize flow collected from detectors
        station_file_red = station_file_merged[['begin', 'end', 'id', 'flow', 'speed', 'occupancy']].copy()
        station_file_red.loc[:, 'flow_all'] = station_file_red[['flow']].sum(axis=1)
        station_file_red[['speed']] = station_file_red[['speed']].replace(-1, np.nan, inplace=False)
        station_file_red['speed_all'] = station_file_red[['speed']].mean(axis=1)
        station_file_red['occupancy_all'] = station_file_red[['occupancy']].mean(axis=1)

        station_flow = station_file_red[['flow_all']]
        station_speed = station_file_red[['speed_all']]
        station_occupancy = station_file_red[['occupancy_all']]

        station_flow.columns = [station]
        station_speed.columns = [station]
        station_occupancy.columns = [station]

        flow_all = pd.concat([flow_all, station_flow], axis=1)
        speed_all = pd.concat([speed_all, station_speed], axis=1)
        occupancy_all = pd.concat([occupancy_all, station_occupancy], axis=1)

    return flow_all, speed_all, occupancy_all

def data_loader_ramp():
    flow_all = pd.DataFrame()
    speed_all = pd.DataFrame()
    occupancy_all = pd.DataFrame()

    # loop through all stations in the station_list
    for station in station_ramp_list:
        station_file = {}
        for file in os.listdir(csv_dict):
            if station in file:
                station_file[file] = pd.read_csv(os.path.join(csv_dict, file))
        print(station + " file loaded successfully")
        station_file_merged = pd.concat(station_file.values(), axis=1)

        # summarize flow collected from detectors
        station_file_red = station_file_merged[['begin', 'end', 'id', 'flow', 'speed', 'occupancy']].copy()
        station_file_red.loc[:, 'flow_all'] = station_file_red[['flow']].sum(axis=1)
        station_file_red[['speed']] = station_file_red[['speed']].replace(-1, np.nan, inplace=False)
        station_file_red['speed_all'] = station_file_red[['speed']].mean(axis=1)
        station_file_red['occupancy_all'] = station_file_red[['occupancy']].mean(axis=1)

        station_flow = station_file_red[['flow_all']]
        station_speed = station_file_red[['speed_all']]
        station_occupancy = station_file_red[['occupancy_all']]

        station_flow.columns = [station]
        station_speed.columns = [station]
        station_occupancy.columns = [station]

        flow_all = pd.concat([flow_all, station_flow], axis=1)
        speed_all = pd.concat([speed_all, station_speed], axis=1)
        occupancy_all = pd.concat([occupancy_all, station_occupancy], axis=1)

    return flow_all, speed_all, occupancy_all

flow_all, _, _ = data_loader_main()

print(flow_all)




