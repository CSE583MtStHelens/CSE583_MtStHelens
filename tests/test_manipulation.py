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


    def test_stack_in_time(self):
        """
        Test the stackInTime function 
        Creates synthetic data and tests whether the funciton runs without errors
        Tests for negative data, and some stations lacking all the data
        Ensures that the type and shape of the output data is as expected and that the original df is unaltered
        """
        # Create a sample DataFrame for testing
        dates = pd.date_range(start='2001-01-01', end='2004-01-05', freq='10T')
        df = pd.DataFrame({
            'Station1': np.random.randn(len(dates)),
            'Station2': 100 * np.random.randn(len(dates)) - 50,
            'Station3': np.random.randn(len(dates)),
        }, index=dates)
        df['Station3']['2004-01-05 09:30:40'] = None
        df_copy = df.copy()

        # Test if the function runs without errors
        seasonal_data, data_no_seasonal = mf.stackInTime(df)

        # Check if the output types are as expected
        self.assertIsInstance(seasonal_data, pd.DataFrame)
        self.assertIsInstance(data_no_seasonal, pd.DataFrame)

        # Check if the output DataFrames have the correct shape
        self.assertEqual(seasonal_data.shape, (24 * 6 * 365, 3))  #  24 hours * 6 10-minute intervals * 365 days
        self.assertEqual(data_no_seasonal.shape, df.shape)

        # Check if the input DataFrame is not modified
        self.assertTrue(df.equals(df_copy))

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



