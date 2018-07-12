import unittest
import json
import csv
from find_contacts_at_companies_fn import find_contacts_at_companies

class FindContactsTestCase(unittest.TestCase):
    """Tests find_contacts_at_companies_fn.py"""

    # Remember, test methods must begin with the word "test."
    def test_1(self):
        """When the input_filename is passed to the  
        function, does the returned results_list match the 
        corresponding output_list_answer.json?"""
        
        input_filename_companies = 'test_files/input_data_companies_test2.csv'
        input_filename_contacts = 'test_files/input_data_contacts_test2.csv' 
      
        (results_contacts, results_companies) = find_contacts_at_companies(
            input_filename_companies, input_filename_contacts
            )

        right_answer_file1 = 'test_files/output_companies_answer2.json'
        with open(right_answer_file1) as f_obj:
            right_companies_answer1 = json.load(f_obj)

        right_answer_file2 = 'test_files/output_contacts_answer2.json'
        with open(right_answer_file2) as f_obj:
            right_contacts_answer1 = json.load(f_obj)

        self.assertEqual(
            (results_contacts, results_companies),
            (right_contacts_answer1, right_companies_answer1)
            )

unittest.main()