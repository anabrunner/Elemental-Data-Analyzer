import pathlib
import csv
from datetime import datetime

#Reads csv file copied from ICP-OES software and saves data as a dictionary.
def get_data(file_path):
    icp_data = {}
    file = open(file_path, "r")
    #This is to read the header line so that it is excluded from the loop for each row in file.
    file.readline()
    for row in file:
        columns = row.split(",")
        icp_data[columns[0]] = {
            "Al, ppm" : columns[1],
            "Ba, ppm" : columns[2],
            "Ca, ppm" : columns[3],
            "K, ppm" : columns[4],
            "Mg, ppm" : columns[5],
            "Mo, ppm" : columns[6],
            "Na, ppm" : columns[7],
            "Ni, ppm" : columns[8],
            "Ti, ppm" : columns[9],
            "Zn, ppm" : columns[10]
        }
    file.close()
    return icp_data

#Sorts the samples into lists with just the respective sample types.
def sort_samples(samples_list):
    standards = ["Blank", "Standard 1", "Standard 2", "Standard 3", "Continuing Calibration Blank", "Continuing Calibration Verification"]
    aquarium_samples_list = []
    river_samples_list = []
    lake_samples_list = []
    other_samples_list = []
    for sample in samples_list:
        if sample in standards:
            pass
        elif sample[0].upper() == "A":
            aquarium_samples_list.append(sample)
        elif sample[0].upper() == "R":
            river_samples_list.append(sample)
        elif sample[0].upper() == "L":
            lake_samples_list.append(sample)
        else:
            other_samples_list.append(sample)
    return aquarium_samples_list, river_samples_list, lake_samples_list, other_samples_list

#Config used by function for different types of analysis.
config = {
    "aquarium" : ["K, ppm", "Mo, ppm", "Ni, ppm", "Na, ppm", "Ba, ppm", "Zn, ppm"],
    "river" :  ["K, ppm", "Ni, ppm", "Mo, ppm", "Ca, ppm", "Na, ppm", "Al, ppm", "Mg, ppm", "Zn, ppm"],
    "lake" : ["K, ppm", "Ni, ppm", "Mo, ppm", "Na, ppm", "Ti, ppm", "Zn, ppm"],
    "other" : ["K, ppm", "Ni, ppm", "Mo, ppm", "Ca, ppm", "Na, ppm", "Al, ppm", "Mg, ppm", "Zn, ppm", "Ba, ppm", "Ti, ppm"]
}

#Writes a csv file with just the respective sample type.
def write_csv(data, sample_list, type):
    if sample_list == []:
        return
    headers = ["Sample"] + config[type]
    rows = []
    counter = 1
    file_name = f"{type} {now} {counter}.csv"
    file_path = pathlib.Path(__file__).parent / type / file_name
    #Checks if the file already exists to prevent overwriting.
    while file_path.is_file():
        counter += 1
        file_name = f"{type} {now} {counter}.csv"
        file_path = pathlib.Path(__file__).parent / type / file_name
    for sample in data:
        if sample in sample_list:
            sample_data = {
                "Sample" : sample
            }
            for item in config[type]:
                sample_data[item] = data[sample][item]
            rows.append(sample_data)
    with open(file_path, "w+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return f

#Message upon running script to explain to user what will happen.
print("Hello! Welcome to the Elemental Data Analyzer!")
print("This script will analyze all .csv files in the same folder that this script is saved in.")
print("Processed files will be saved in their respective sample type folders, and original files will be moved to the Raw Data folder.")
print("Press 'Enter' to continue!")
input()

#Gets today's date to append to file name for ease of finding.
now = str(datetime.now().strftime("%Y%m%d"))

#Searches directory for files with .csv extension and appends it to a list.
data_path = pathlib.Path(__file__).parent
data_files = []
for file in data_path.glob("*.csv"):
    data_files.append(file.name)

#Error message to user in case no files were found.
if data_files == []:
    print("Ooops! It appears no files were found! Please check that the data files have a .csv extension.")
    print("Press 'Enter' to close this window.")
    input()
else:
    #Loops through the data files found.
    for file in data_files:
        data_path = pathlib.Path(__file__).parent / file
        icp_data = get_data(data_path)
        #Writes a list of all the samples in this file.
        samples_list = list(icp_data.keys())
        #Runs the functions, output will be separate .csv files.
        write_csv(icp_data, sort_samples(samples_list)[0], "aquarium")
        write_csv(icp_data, sort_samples(samples_list)[1], "river")
        write_csv(icp_data, sort_samples(samples_list)[2], "lake")
        write_csv(icp_data, sort_samples(samples_list)[3], "other")
        #Moves raw data file to archive folder once its done processing.
        new_path = pathlib.Path(__file__).parent / "Raw data" / file
        data_path.rename(new_path)
