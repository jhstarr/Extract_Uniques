import unittest
import json
import csv
from extract_unique_fn import get_uniques

class FlattenerTestCase(unittest.TestCase):
    """Tests for extract_unique_fn.py"""

    # Remember, test methods must begin with the word "test."
    def test_case_1(self):
        """When the input_filename is passed to the get_uniques() 
        function, does the returned results_list match the 
        corresponding output_list_answer.json?"""
        
        input_filename1 = 'test_files/input_data_with_dupes_test1.csv' 
      
        results_list1 = get_uniques(input_filename1)

        right_answer_file1 = 'test_files/output_list_answer1.json'
        with open(right_answer_file1) as f_obj:
            right_answer1 = json.load(f_obj)

        self.assertEqual(results_list1,right_answer1)

    def test_case_2(self):
        """When the input_filename is passed to the get_uniques() 
        function, does the returned results_list match the 
        corresponding output_list_answer.json?"""
        
        input_filename2 = 'test_files/input_data_with_dupes_test2.csv' 
      
        results_list2 = get_uniques(input_filename2)

        right_answer_file2 = 'test_files/output_list_answer2.json'
        with open(right_answer_file2) as f_obj:
            right_answer2 = json.load(f_obj)

        self.assertEqual(results_list2,right_answer2)













unittest.main()