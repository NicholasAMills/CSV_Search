'''
Description: You're looking for a car but only in a specific color. There is a list of colors you want in file "input1.csv". There exists a file "compare_file1.csv" which contains a list of cars and their details, including color, on column 3. 
Iterate through "input1.csv" and search for matching SKU's in "compare_file1.csv". If there is a match, store the matching SKU row's data in "output_matches1.csv" as a new row. If there is no match found, store the SKU in csv file "unmatched1.csv"
'''
from csv import reader, writer
import timeit

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
    COMPARE_TO = 'compare_to/car_list.csv'
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
        # Count rows in input csv file
        row_count = 0
        for row in open(INPUT):
            row_count += 1

        # Read input and compare csv files and store data in lists to work with
        with open(INPUT, 'r') as input, open(COMPARE_TO) as compare:
            try:
                print("Reading file one....")
                fileone = reader(input)
                for row in fileone:
                    fileone_list.append(row[0]) # index 0 to get number. If ommited, result would be ['0001'] when we're looking for 0001
                print("Reading file two....")
                filetwo = reader(compare)
                for row in filetwo:
                    filetwo_list.append(row) # we want the whole row since we'll be storing the entire row in the matches csv file if we find a match
                print("Done")
            except Exception as e:
                print("Error occurred in reading files: " + str(e))
        
        # Index counter for progress
        index = 1
        # Iterate through our input list and search each index for a match in our compare list
        for row in fileone_list:
            try:
                print("==========================================")
                print("Progress: " + str(index) + "/" + str(row_count))
                print("Searching for " + str(row))
                # boolean for print statement
                found = False
                # Iterate through file two in search for "row"
                for line_num, content in enumerate(filetwo_list):
                    if content[2] == row: # We know the input we're looking for will be in the 3rd column
                        found = True
                        print("FOUND")
                        # Create a list to capture the specific column data we want
                        found_data = []
                        # Save entire row
                        for i in content:
                            found_data.append(i)

                        # OR to only save specific columns
                        # found_data.append(content[0])
                        # found_data.append(content[1])
                        # found_data.append(content[2])
                        # found_data.append(content[3])

                        # Append found_data to matches list
                        matches.append(found_data)
                if not found:
                    unmatches.append([row])
                    print("NOT FOUND")
            except Exception as e:
                print("There was an exception while searching: " + str(e))
                pass
            finally:
                index += 1
        
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
            print(fileone_list[0], filetwo_list[1])
        except Exception as e:
            print("Exception occurred in finally: " + str(e))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception occurred starting program" + str(e))