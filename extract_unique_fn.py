# Jeff Starr, 18 September, 2017
# This is a program that takes a csv file and returns a csv file
# containing the unique elements, sorted naturally.
# It expects the file to be a sparse matrix of numbers or a sparse matrix
# of strings.  It can be mixed.  The matrix can be a single column.

from natsort import natsorted, ns
import csv

def get_uniques(input_filename):

    my_list = []
    new_list = []

    with open(input_filename, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            for item in row:
                if item == '':
                    pass
                else:
                    my_list.append(item)
       

    # This produces a new_list of uniques.
    for item in my_list:
        if item in new_list:
            pass
        else:
            new_list.append(item)

    new_list = natsorted(new_list, key=lambda y: y.lower())

    return new_list