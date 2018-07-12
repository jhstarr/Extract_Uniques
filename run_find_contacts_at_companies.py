# Jeff Starr, 4 October, 2017

# This is a program that calls the find_contacts_at_companies_fn then 
# writes the output to a file.

# Instructions:
# Copy the two input files into a new google spreadsheet.
# Save as csv called input_data_companies_<something>.csv and 
# input_data_contacts_<something>.csv into 
# Projects/PRODUCTION_Data/Find_Contacts_at_Companies_data.  Run the program.  
# Copy results out of Output file or drag into google sheets.

import csv
import json
import os
from find_contacts_at_companies_fn import find_contacts_at_companies
 

input_companies_fname = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Find_Contacts_at_Companies_data/" +
#    "input_data_companies_test2.csv"
    "input_data_companies_glmaster3Jul.csv"
    )

input_contacts_fname = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Find_Contacts_at_Companies_data/" +
#    "input_data_contacts_test2.csv"
    "input_data_contacts_cm.csv"
    )

output_filename1 = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Find_Contacts_at_Companies_data/" +
#    "output_data_contacts_at_companies_test2.csv"
    "output_data_contacts_at_companies_glcm2.csv"
    )

output_filename2 = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Find_Contacts_at_Companies_data/" +
    "output_data_companies_with_contacts_test2.csv"
 #   "output_data_companies_with_contacts_glcm2.csv"
    )


(contacts_at_companies, companies_with_contacts) = find_contacts_at_companies(
    input_companies_fname, input_contacts_fname
    )


# Note that writerow expects a sequence. The square brackets around row
# prevents writerow from placing each character in its own column.

with open(output_filename1, 'w', encoding='utf-8') as f_write:
    writer = csv.writer(f_write)
    for row in contacts_at_companies:
        writer.writerow(row)

with open(output_filename2, 'w', encoding='utf-8') as f_write:
    writer = csv.writer(f_write)
    for row in companies_with_contacts:
        writer.writerow([row])


# The following writes the output_list as json to a file so that it can be
# checked by a human then used for testing.  When you want to run a new test
# case, uncomment and run this code then comment it back.

"""
output_json_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/github/" +
    "Find_Contacts_at_Companies/test_files/output_contacts_answer2.json"
    )
with open(output_json_filename, 'w') as outfile:
    json.dump(contacts_at_companies, outfile)

output_json_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/github/" +
    "Find_Contacts_at_Companies/test_files/output_companies_answer2.json"
    )
with open(output_json_filename, 'w') as outfile:
    json.dump(companies_with_contacts, outfile)
"""


