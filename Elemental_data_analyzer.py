import pathlib
import csv
from datetime import datetime

#Asks user to input file name.
print("Welcome to the automated elemental data analyzer for lake, river, and aquarium samples!") 
print("Please type below the name of the file to be analyzed.")
print("It should be in the same folder as this script and include the .csv extension!")
print("For example: testdata.csv")
user_file = input()
file_path = pathlib.Path(__file__).parent / user_file

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

icp_data = get_data(file_path)

#Writes a list of all samples.
samples_list = list(icp_data.keys())

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

#Gets today's date and time to append to file name and avoid overwriting previous data.
now = str(datetime.now().strftime("%Y%m%d%H%M"))

#Writes a csv file with just the respective sample type.
def aquarium_samples(data, sample_list):
    if sample_list == []:
        return
    aquarium_headers = ["Sample", "K, ppm", "Mo, ppm", "Ni, ppm", "Na, ppm", "Ba, ppm", "Zn, ppm"]
    aquarium_rows = []
    file_name = "Aquarium %s.csv" % now
    for sample in data:
        if sample in sample_list:
            sample_data = {
                "Sample" : sample,
                "K, ppm" : data[sample]["K, ppm"],
                "Mo, ppm" : data[sample]["Mo, ppm"],
                "Ni, ppm" : data[sample]["Ni, ppm"],
                "Na, ppm" : data[sample]["Na, ppm"],
                "Ba, ppm" : data[sample]["Ba, ppm"],
                "Zn, ppm" : data[sample]["Zn, ppm"]
            }
            aquarium_rows.append(sample_data)
    with open(pathlib.Path(__file__).parent/ "Aquarium" / file_name, "w+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=aquarium_headers)
        writer.writeheader()
        writer.writerows(aquarium_rows)
    return f

def river_samples(data, sample_list):
    if sample_list == []:
        return
    river_headers = ["Sample", "K, ppm", "Ni, ppm", "Mo, ppm", "Ca, ppm", "Na, ppm", "Al, ppm", "Mg, ppm", "Zn, ppm"]
    river_rows = []
    file_name = "River %s.csv" % now
    for sample in data:
        if sample in sample_list:
            sample_data = {
                "Sample" : sample,
                "K, ppm" : data[sample]["K, ppm"],
                "Ni, ppm" : data[sample]["Ni, ppm"],
                "Mo, ppm" : data[sample]["Mo, ppm"],
                "Ca, ppm" : data[sample]["Ca, ppm"],
                "Na, ppm" : data[sample]["Na, ppm"],
                "Al, ppm" : data[sample]["Al, ppm"],
                "Mg, ppm" : data[sample]["Mg, ppm"],
                "Zn, ppm" : data[sample]["Zn, ppm"]
            }
            river_rows.append(sample_data)
    with open(pathlib.Path(__file__).parent / "River" / file_name, "w+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=river_headers)
        writer.writeheader()
        writer.writerows(river_rows)
    return f

def lake_samples(data, sample_list):
    if sample_list == []:
        return
    lake_headers = ["Sample", "K, ppm", "Ni, ppm", "Mo, ppm", "Na, ppm", "Ti, ppm", "Zn, ppm"]
    lake_rows = []
    file_name = "Lake %s.csv" % now
    for sample in data:
        if sample in sample_list:
            sample_data = {
                "Sample" : sample,
                "K, ppm" : data[sample]["K, ppm"],
                "Ni, ppm" : data[sample]["Ni, ppm"],
                "Mo, ppm" : data[sample]["Mo, ppm"],
                "Na, ppm" : data[sample]["Na, ppm"],
                "Ti, ppm" : data[sample]["Ti, ppm"],
                "Zn, ppm" : data[sample]["Zn, ppm"]
            }
            lake_rows.append(sample_data)
    with open(pathlib.Path(__file__).parent / "Lake" / file_name, "w+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=lake_headers)
        writer.writeheader()
        writer.writerows(lake_rows)
    return f

def other_samples(data, sample_list):
    if sample_list == []:
        return
    other_headers = ["Sample", "K, ppm", "Ni, ppm", "Mo, ppm", "Ca, ppm", "Na, ppm", "Al, ppm", "Mg, ppm", "Zn, ppm", "Ba, ppm", "Ti, ppm"]
    other_rows = []
    file_name = "Other %s.csv" % now
    for sample in data:
        if sample in sample_list:
            sample_data = {
                "Sample" : sample,
                "K, ppm" : data[sample]["K, ppm"],
                "Ni, ppm" : data[sample]["Ni, ppm"],
                "Mo, ppm" : data[sample]["Mo, ppm"],
                "Ca, ppm" : data[sample]["Ca, ppm"],
                "Na, ppm" : data[sample]["Na, ppm"],
                "Al, ppm" : data[sample]["Al, ppm"],
                "Mg, ppm" : data[sample]["Mg, ppm"],
                "Zn, ppm" : data[sample]["Zn, ppm"],
                "Ba, ppm" : data[sample]["Ba, ppm"],
                "Ti, ppm" : data[sample]["Ti, ppm"]
            }
            other_rows.append(sample_data)
    with open(pathlib.Path(__file__).parent / "Other" / file_name, "w+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=other_headers)
        writer.writeheader()
        writer.writerows(other_rows)
    return f

#Runs the functions, output will be separate csv files.
aquarium_samples(icp_data, sort_samples(samples_list)[0])
river_samples(icp_data, sort_samples(samples_list)[1])
lake_samples(icp_data, sort_samples(samples_list)[2])
other_samples(icp_data, sort_samples(samples_list)[3])

#Moves raw data file to archive folder oncce its done processing.
file_path.rename(pathlib.Path(__file__).parent / "Raw data" / user_file)