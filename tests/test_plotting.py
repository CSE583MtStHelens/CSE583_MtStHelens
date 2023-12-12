"""
Test file for the plotting_function.py but only the functions
which do not output a plot.
"""
import unittest
import sys
import os
import numpy as np
import pandas as pd

#file directory manipulation - relative import
current_directory = os.getcwd()
# Go back one folder level
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.insert(0, parent_directory)
from mtsthelens import plotting_functions

# Define a class in which the tests will run
class Test_Plotting(unittest.TestCase):
    """This class contains all test for the functions in plotting_functions.py"""
    def setUp(self):
        # Create sample DataFrames for testing
        self.df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        self.df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
        self.empty_dict = {}
        self.non_dict = "Not a dictionary"
        self.non_dataframe_dict = {'df1': self.df1, 'df2': "Not a DataFrame"}

    def test_min_mak_values_smokey(self):
        """Smoke Test and at the same time also a one-shot test 
        for only positive float values for calculate_distance-function."""

    def test_min_max_values(self):
        # Test with valid input
        input_dict = {'df1': self.df1, 'df2': self.df2}
        min_df, max_df = plotting_functions._min_max_values(input_dict)
        # Assertions
        self.assertTrue(isinstance(min_df, pd.DataFrame))
        self.assertTrue(isinstance(max_df, pd.DataFrame))
        self.assertEqual(min_df.shape, (3, 2))
        self.assertEqual(max_df.shape, (3, 2))

    def test_empty_dictionary(self):
        # Test with an empty dictionary
        with self.assertRaises(ValueError):
            plotting_functions._min_max_values(self.empty_dict)

    def test_non_dict_input(self):
        # Test with a non-dictionary input
        with self.assertRaises(TypeError):
            plotting_functions._min_max_values(self.non_dict)

    def test_non_dataframe_values(self):
        # Test with a dictionary containing non-DataFrame values
        with self.assertRaises(TypeError):
            plotting_functions._min_max_values(self.non_dataframe_dict)
