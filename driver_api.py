'''
Description: You're looking for a car but only in a specific color. There is a list of colors you want in file "input1.csv". There exists a file "compare_file1.csv" which contains a list of cars and their details, including color, on column 3. 
Iterate through "input1.csv" and search for matching SKU's in "compare_file1.csv". If there is a match, store the matching SKU row's data in "output_matches1.csv" as a new row. If there is no match found, store the SKU in csv file "unmatched1.csv"
'''
from csv import reader, writer
import datetime
import timeit
import urllib3
import requests

'''
write data to csv files
data: the list of data to be written
file: the file the data will be written to
isMatch: differentiate between matches and unmatched. Used for writing header in the csv files
'''
def writeToCsv(data, file, isMatch):
    try:
        with open(file, 'w', newline='') as f_object:
            writer_object = writer(f_object)
            # write header
            if isMatch:
                match_csv_header = ["ID", "NAME", "COLOR", "BRAND"]
                writer_object.writerow([match_csv_header[0], match_csv_header[1], match_csv_header[2], match_csv_header[3]])
            else:
                writer_object.writerow(["COLOR"])

            # Write data
            for index in data:
                writer_object.writerow(index)
            f_object.close()
    except Exception as e:
        print("Exception occurred in writeToCSV: " + str(e))

def main():
    # CSV files - currently set up to work with one input file, one match file and one unmatched file
    INPUT = 'input/colors.csv'
    MATCHED = 'matches/output_matches_colors.csv'
    UNMATCHED = 'unmatched/unmatched_colors.csv'

    # Timer
    start = timeit.default_timer()

    # Store data for matches and unmatched inputs
    matches = []
    unmatches = []

    # Read data from csv files and store them here
    fileone_list = []
    filetwo_list = []

    try:
        # Disable warnings in console
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Count rows in input csv file
        row_count = 0
        for row in open(INPUT):
            row_count += 1
        
        with open(INPUT, 'r') as input:
            csv_reader = reader(input)
            # Counter for user visualization
            index = 1
            for row in csv_reader:
                try:
                    print("==========================================")
                    print("Progress: " + str(index) + "/" + str(row_count))
                    print("Searching for " + str(row))
                    url = 'www.example-api.com'
                    payload = {}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                    responseJSON = response.json()
                    # if responseJSON has 'features' (json entry example which determines if data exists) and is not empty, a match has been found
                    if responseJSON['features'] and responseJSON['features'] != "":
                        # Loop through 'features' in cases where data includes multiple 'attributes' entries
                        for feature in responseJSON['features']:
                            feature_data = []
                            # Get epoch time (milliseconds)
                            epoch_time = feature['attributes']['EPOCHDATE']
                            # If epoch time has numeric value, convert it to datetime
                            if type(epoch_time) == int:
                                # Convert to datetime passin in epoch_time as seconds
                                ts = datetime.datetime.fromtimestamp(epoch_time/1000).strftime('%m-%d-Y %H:%M:%S')
                                # update the json data
                                feature['attributes']['EPOCHDATE'] = ts
                            # Gather specific data in feature_data list (note: this is example data. This doesn't exist)
                            feature_data.append(feature['attributes']['GLOBALID'])
                            feature_data.append(feature['attributes']['COMPANYID'])
                            feature_data.append(feature['attributes']['EPOCHDATE'])
                            feature_data.append(feature['attributes']['BARCODE'])
                            # Append feature_data list to matches list
                            matches.append(feature_data)
                        print("FOUND")
                    else:
                        unmatches.append([row[0]])
                        print("NOT FOUND")
                except Exception as e:
                    print(e)
        
    except Exception as e:
        print("Exception occured in main(): " + str(e))

    finally:
        try:
            print("==========================================")
            print("WRITING TO " + str(MATCHED) + " ....")
            writeToCsv(matches, MATCHED, True)
            print("WRITING TO " + str(UNMATCHED) + " ....")
            writeToCsv(unmatches, UNMATCHED, False)
            print("===============COMPLETE===================")
            stop = timeit.default_timer()
            print("Execution time: ", stop - start)
        except Exception as e:
            print("Exception occurred in finally: " + str(e))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception occurred starting program" + str(e))