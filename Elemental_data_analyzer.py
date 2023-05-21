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
    file_name = "%s %s.csv" % (type, now)
    for sample in data:
        if sample in sample_list:
            sample_data = {
                "Sample" : sample
            }
            for item in config[type]:
                sample_data[item] = data[sample][item]
            rows.append(sample_data)
    with open(pathlib.Path(__file__).parent / type / file_name, "w+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return f

#Runs the functions, output will be separate csv files.
write_csv(icp_data, sort_samples(samples_list)[0], "aquarium")
write_csv(icp_data, sort_samples(samples_list)[1], "river")
write_csv(icp_data, sort_samples(samples_list)[2], "lake")
write_csv(icp_data, sort_samples(samples_list)[3], "other")

#Moves raw data file to archive folder oncce its done processing.
file_path.rename(pathlib.Path(__file__).parent / "Raw data" / user_file)