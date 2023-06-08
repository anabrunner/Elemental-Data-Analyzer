# Elemental-Data-Analyzer
A script for sorting and cleaning data from chemical analysis.

A lab runs routine ICP-OES analysis on different water samples to measure elemental composition. The samples can be from an aquarium, river, or lake water source. Each water source has different reporting requirements even though they are analyzed together, in no particular order. This script cleans up and sorts the sample data, organizing like samples into a single file with just the required reporting elements.

** Version 2.0 **
New in this version:
- To use this script, save the .csv files to be analyzed in the same folder as this script.
- Double click to run the script.
- The files in the folder will automatically be analyzed (multiple files can be analyzed at once now).
- Files will be written into the respective sample type folders.
- Naming convention for the files written will be "[TYPE] [YYYYMMDD] [#]".
- The # will be incremented with each analysis to prevent file overwriting.
- If multiple files are analyzed at once, multiple files may be created for each sample type.
	- This is depending on whether multiple files had samples for the same sample type.
- If no files are found in the folder, a window will pop up with an error message. Press enter to close it.