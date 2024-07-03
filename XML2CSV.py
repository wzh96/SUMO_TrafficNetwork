import os
import xml.etree.ElementTree as ET
import csv

def xml_to_csv(xml_file, path = 'Sim_Results/Ramp_Random/'):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract detector data
    detector_data = []
    for interval in root.findall('.//interval'):
        data = {
            'begin': interval.get('begin'),
            'end': interval.get('end'),
            'id': interval.get('id'),
            'nVehContrib': interval.get('nVehContrib'),
            'flow': interval.get('flow'),
            'occupancy': interval.get('occupancy'),
            'speed': interval.get('speed'),
            'harmonicMeanSpeed': interval.get('harmonicMeanSpeed'),
            'length': interval.get('length'),
            'nVehEntered': interval.get('nVehEntered')
        }
        detector_data.append(data)

    # Write detector data to CSV
    csv_file = path + os.path.splitext(os.path.basename(xml_file))[0] + '.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['begin', 'end', 'id', 'nVehContrib', 'flow', 'occupancy', 'speed', 'harmonicMeanSpeed', 'length', 'nVehEntered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in detector_data:
            writer.writerow(data)

    print(f"CSV file generated: {csv_file}")


