'''
Description: Append new columns to a base .csv file from data found in an input .csv file by searching for matching values and comparing key identifiers

Details: The Updated_Features.csv file has data that needs to be appended to the Full_Inventory.csv file. Vehicle color for each vehicle model is specific to which location it came from and is therefore an identifier.
    I.e a "green" RD02 can only be found at Location 1, but RD02's can be found in all locations and all are still a model_id 1
Use the model ids and location values to update the base file accordingly.

Directories:
  base - the file you want to make changes to

  input - the file in which you're comparing and pulling data from

  output - updated base file based on matching data found in input file
'''
from cmath import isnan
import pandas as pd
import numpy as np
import math
import timeit

def main():
    # CSV files - currently set up to work with one input file, one match file and one unmatched file
    INPUT = 'input/Updated_Features.csv'
    BASE = 'base/Full_Inventory.csv'
    OUTPUT = 'output/output_Full_Inventory.csv'

    # Read .csv files and store them as pandas dataframes
    compare_df = pd.read_csv(BASE)
    input_df = pd.read_csv(INPUT)

    # New dataframe to hold new data
    result_df = pd.DataFrame()

    # Timer
    start = timeit.default_timer()
    for index, row in compare_df.iterrows():
        try:
            # BASE file's desired column to be searched
            model_id = row['MODEL_ID']
            location = float(row['LOCATION'])

            # If car exists in multiple locations, check the location for match and store the location in a list (It will only be a list length of 1, containing the location in the .csv file)
            if math.isnan(location):
                current_list = input_df.loc[input_df['model_id'] == model_id].index.tolist()
            else:
                current_list = input_df.loc[(input_df['model_id'] == model_id) & (input_df['location'] == location)].index.tolist()

            for item in current_list:
                # Set desired columns to append to the base file here.
                result_df.at[index, 'name'] = input_df.at[item, 'name']
                result_df.at[index, 'address'] = input_df.at[item, 'address']
                result_df.at[index, 'phone'] = input_df.at[item, 'phone']
                
                if index % 100 == 0:
                    print(str(index) + "/" + str(len(compare_df)-1))
                    stop = timeit.default_timer()
                    print("Time: ", stop - start)
        except Exception as e:
            print("Bad data on line " + str(index) + ": " + str(e))

    # Concatenate the two dataframes
    dfs = [compare_df, result_df]
    compare_df = pd.concat(dfs, axis=1).reindex(compare_df.index)

    # Write to new csv file
    compare_df.to_csv(OUTPUT, index=False)
    print(str(index) + "/" + str(len(compare_df)-1))
    print("==========COMPLETE==========")
    stop = timeit.default_timer()
    print("Completion time: ", stop - start)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception occurred starting program" + str(e))