# Jeff Starr, 4 October, 2017

# This is a program that calls the extract_unique_fn then 
# writes the data returned to a file.

# Instructions:
# Copy the data to de-dupe into a new google spreadsheet.
# Save as csv called input_data_with_dupes<something>.csv and save into 
# Projects/PRODUCTION_Data/Extract_uniques_data.  Run the program.  Copy results out of Output file
# or drag into google sheets.

import csv
import json
import os
from extract_unique_fn import get_uniques
 

input_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Extract_uniques_data/" +
    "input_data_with_dupes_918.csv"
    )

output_list_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Extract_uniques_data/" +
    "output_data_no_dupes_918.csv"
    )

output_list = get_uniques(input_filename)


# Note that writerow expects a sequence. The square brackets around row
# prevents writerow from placing each character in its own column.

with open(output_list_filename, 'w', encoding='utf-8') as f_write:
    writer = csv.writer(f_write)
    for row in output_list:
        writer.writerow([row])


# The following writes the output_list as json to a file so that it can be
# checked by a human then used for testing.

"""
output_json_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "Extract_Unique_Numbers/test_files/output_list_answer1.json"
    )
with open(output_json_filename, 'w') as outfile:
    json.dump(output_list, outfile)
"""