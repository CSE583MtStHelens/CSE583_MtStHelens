"""This python file contains the tests for the preprocessing functions."""
import unittest
import numpy as np
import pandas as pd
import datetime
import sys, os

# File directory preprocessing - relative import
current_directory = os.getcwd()
# Go back one folder level
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.insert(0, parent_directory)
from mtsthelens import preprocessing_functions

# This script includes test to test the preprocessing functions.
# To run the test navigate into the directory
# You can eighter type 'python -m unittest discover' or 
# specify the folder with 'python -m unittest discover -s tests'

# Define a class in which the tests will run
class TestPreprocessingFunctions(unittest.TestCase):
    # Tests for calculate_distance
    def test_calculate_distance_A(self):
        """Smoke Test and at the same time also a one-shot test 
        for only positive float values for calculate_distance-function."""
        lat1 = 0
        lat2 = 180
        lon1 = 0
        lon2 = 180

        result = preprocessing_functions.calculate_distance(lat1, lat2, lon1, lon2)

        self.assertAlmostEqual(result, 0.0, places=6) 

    def test_calculate_distance_B(self):
        """One-shot test for only positive and negative integer and float 
        values for calculate_distance-function."""
        lat1 = 0.0
        lat2 = -180.0
        lon1 = 0
        lon2 = 180

        result = preprocessing_functions.calculate_distance(lat1, lat2, lon1, lon2)

        self.assertAlmostEqual(result, 0.0, places=6) 

    def test_calculate_distance_C(self):
        """Test if input is a string. """
        lat1 = 0
        lat2 = 0
        lon1 = 0
        lon2 = 'zero'

        with self.assertRaises(TypeError):
            preprocessing_functions.calculate_distance(lat1, lat2, lon1, lon2)

    def test_calculate_distance_D(self):
        """Test if input is a list. """
        lat1 = 0
        lat2 = 0
        lon1 = 0
        lon2 = [0,180]

        with self.assertRaises(TypeError):
            preprocessing_functions.calculate_distance(lat1, lat2, lon1, lon2)
    
    def test_calculate_distance_E(self):
        """Test if input is a pd.Series. """
        lat1 = 0
        lat2 = 0
        lon1 = 0
        lon2 = pd.Series([0,180])

        with self.assertRaises(TypeError):
            preprocessing_functions.calculate_distance(lat1, lat2, lon1, lon2)
    
    # Tests for mask_df
    def test_mask_df_A(self):
        """Smoke Test and at the same time also a one-shot test 
        for only positive values for mask_df-function."""
        idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
        df_test = pd.Series(0, index=idx)
        df_test.iloc[4000]= 1

        masked_df_test = preprocessing_functions.mask_df(df_test)
        result = np.sum(masked_df_test)

        self.assertAlmostEqual(result, 0.0, places=6) 

    def test_mask_df_B(self):
        """One-shot test for only positive values for mask_df-function."""
        idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
        df_test = pd.Series(0, index=idx)
        df_test.iloc[4000]= 1

        masked_df_test = preprocessing_functions.mask_df(df_test)
        result = sum(masked_df_test)

        self.assertTrue(np.isnan(result)) 

    # def test_mask_df_C(self):
    #     """One-shot test for only negative values for mask_df-function."""
    #     idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
    #     df_test = pd.Series(0, index=idx)
    #     df_test.iloc[4000]= -1

    #     masked_df_test = preprocessing_functions.mask_df(df_test)
    #     result = sum(masked_df_test)

    #     self.assertTrue(np.isnan(result)) 

    def test_mask_df_D(self):
        """One-shot test for only positive values if right position masked for mask_df-function."""
        idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
        df_test = pd.Series(0, index=idx)
        df_test.iloc[4000]= 1

        masked_df_test = preprocessing_functions.mask_df(df_test)
        result = np.mean(np.where(np.isnan(masked_df_test)))

        self.assertAlmostEqual(result, 4000, places=1) # uncertainty of +-1

    # def test_mask_df_E(self):
    #     """One-shot test for only positive values if right length masked for mask_df-function."""
    #     idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
    #     df_test = pd.Series(0, index=idx)
    #     df_test.iloc[4000]= 1

    #     masked_df_test = preprocessing_functions.mask_df(df_test)
    #     result = np.where(np.isnan(masked_df_test_small))[0].shape[0]

    #     self.assertAlmostEqual(result, 1000, places=6) # uncertainty of +-2
    
    # Tests for norm
    def test_norm_A(self):
        """Smoke Test and at the same time also a one-shot test 
        for only positive values in a np.array for norm-function."""
        s = np.array([1, 2, 3, 4, 5])
        result = preprocessing_functions.norm(s)
        np.testing.assert_array_almost_equal(result, np.array([0, 0.25, 0.5, 0.75, 1]), decimal=6)

    def test_norm_B(self):
        """One-shot test for negative and positive values in a np.array for norm-function."""
        s = np.array([-10, 0, 10])
        result = preprocessing_functions.norm(s)
        np.testing.assert_array_almost_equal(result, np.array([0, 0.5, 1]), decimal=6)

    def test_norm_C(self):
        """One-shot test for only negative values in a pd.Series for norm-function."""
        s = pd.Series([-10, -5, 0])
        result = preprocessing_functions.norm(s)
        np.testing.assert_array_almost_equal(result, pd.Series([0, 0.5, 1]), decimal=6)

    def test_norm_D(self):
        """Test for empty np.array input for norm-function."""
        s = np.array([])
        with self.assertRaises(ValueError):
            preprocessing_functions.norm(s)

    def test_norm_E(self):
        """Test for empty np.array input for norm-function."""
        s = pd.Series([])
        with self.assertRaises(ValueError):
            preprocessing_functions.norm(s)

    def test_norm_F(self):
        """Test for neither np.array nor pd.Series but df as input for norm-function."""
        s = pd.DataFrame(0, index=range(5), columns=['col1', 'col2'])
        with self.assertRaises(TypeError):
            preprocessing_functions.norm(s)
    
    # def test_read_data(path_file, cols=None):
    
    #     return False
