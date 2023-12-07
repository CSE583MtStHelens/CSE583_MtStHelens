"""
Test file for the manipulation_function.py
"""
import unittest
import sys,os
import numpy as np
import pandas as pd
import pdb

#file directory manipulation - relative import
current_directory = os.getcwd()
# Go back one folder level
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.insert(0, parent_directory)
from mtsthelens import manipulation_functions

class Test_mf(unittest.TestCase):
    def test_smoke_manipulation(self):
        """
        Test the two manipuation functions: stackSpace and StackSpace_yearlyParam will run
        """
        # Create a sample DataFrame for testing
        data = {'Station1': np.random.rand(100),
                'Station2': np.random.rand(100),
                'Station3': np.random.rand(100)}
        df_rsam_median = pd.DataFrame(data, index=pd.date_range('2004-01-01', periods=100, freq='D'))

        #smoke test whether the two functions works
        self.assertIsNone(manipulation_functions.stackInSpace(df_rsam_median))
        df_median_stackSpace, df_stackSpace_year = manipulation_functions.stackInSpace(df_rsam_median)
        self.assertIsNone(manipulation_functions.stackSpace_yearParam(df_stackSpace_year))


    def test_stackInSpace(self):
        """
        Test the stackInSpace function 
        Created the synthetic data and test whether the funciton perform as we expected
        Test if the stackInSpace function stacks data correctly across all stations
        """
        # Create a sample DataFrame for testing
        data = {'Station1': np.random.rand(100),
                'Station2': np.random.rand(100),
                'Station3': np.random.rand(100)}
        df_rsam_median = pd.DataFrame(data, index=pd.date_range('2004-01-01', periods=100, freq='D'))

        # Apply the stackInSpace function
        df_median_stackSpace, df_stackSpace_year = mf.stackInSpace(df_rsam_median)

        # Check if the shape of the stacked DataFrame is correct
        expected_shape = (100, 1)  # Stacking across all stations should result in one column
        self.assertEqual(df_median_stackSpace.shape, expected_shape)

    # Check if the years in the stacked DataFrame match the input DataFrame
        self.assertListEqual(df_stackSpace_year.columns.to_list(), [df_rsam_median.index.year.tolist()[0]])

    def test_stack_space_yearparam(self):
        """
        Test the stack_space_yearparam function 
        Created the synthetic data and test whether the funciton perform as we expected
        """
        # Create a sample DataFrame for testing
        data = {
            'Station1': [10, 20, 30, 40],
            'Station2': [15, 25, 35, 45],
            'Station3': [5, 15, 25, 35]
        }
        df_stackSpace_year = pd.DataFrame(data, index=['01/01 00:00:00', '01/01 01:00:00', '01/01 02:00:00', '01/01 03:00:00'])

        # Test if the function returns a DataFrame with the correct shape
        df_result = mf.stackSpace_yearParam(df_stackSpace_year)

        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertEqual(df_result.shape, (4, 3))  # Adjust the shape based on your expectations

        # Test if the calculated statistics are correct for each column
        expected_max = {'Station1': 40, 'Station2': 45, 'Station3': 35}
        expected_min = {'Station1': 10, 'Station2': 15, 'Station3': 5}
        expected_mean = {'Station1': 25, 'Station2': 30, 'Station3': 20}
        expected_median = {'Station1': 25, 'Station2': 30, 'Station3': 20}

        for col in df_stackSpace_year.columns:
            self.assertAlmostEqual(df_result[col].loc['max'], expected_max[col])
            self.assertAlmostEqual(df_result[col].loc['min'], expected_min[col])
            self.assertAlmostEqual(df_result[col].loc['mean'], expected_mean[col], places=3)
            self.assertAlmostEqual(df_result[col].loc['median'], expected_median[col])



