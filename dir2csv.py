import numpy as np
import pandas as pd
import json
import glob
import csv
import argparse

# Create an ArgumentParser object to specify the arguments for the script
parser = argparse.ArgumentParser(description = "Unite JSON Files to CSV File")

# Adding two arguments - path and name
parser.add_argument('path',type=str, metavar='', help='Path to the folder')
parser.add_argument('name',type=str, metavar='', help="Output file's (CSV format) name")

# Parse the arguments 
args = parser.parse_args()

def dir2csv(path,output_name):
    # Finding the path of all the json files in the specified folder
    find_path = path+ "\*.json"
    files = glob.glob(find_path)
    
    # Read the first file and convert it to a Pandas DataFrame
    with open(files[0], "r") as f:
        combnined_json_df = pd.DataFrame([json.load(f)])
        
    # Create an empty dictionary with the same keys as the columns in the DataFrame        
    empty_dict = {key: None for key in list(combnined_json_df.columns)}
    empty_df = pd.DataFrame.from_dict([empty_dict])
    
    # Add an empty row before and after the input data
    combnined_json_df = pd.concat([empty_df, combnined_json_df, empty_df])
    
    # Loop through the rest of the files and add their contents to the DataFrame
    for index in range(1,len(files)):
        with open(files[index], "r") as f:
            data = json.load(f)
            data_df = pd.DataFrame([data])
            combnined_json_df = pd.concat([combnined_json_df,data_df, empty_df])
            
    # Save the combined DataFrame as a CSV file        
    combnined_json_df.to_csv(output_name, index=False)
    
# Check if the script is being run as the main program      
if __name__ == '__main__':
    # Calling the dir2csv function with the path and name arguments from the command line
    dir2csv(args.path, args.name)