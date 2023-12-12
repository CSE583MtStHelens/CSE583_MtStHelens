"""This python file contains the tests for the preprocessing functions."""
import unittest
import sys
import os
import datetime
import numpy as np
import pandas as pd

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
    """This class contains all test for the functions in preprocessing_functions.py"""
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

    def test_mask_df_C(self):
        """One-shot test for only positive values and test position mask for mask_df-function."""
        idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
        df_test = pd.Series(0, index=idx)
        df_test.iloc[4000]= 1

        masked_df_test = preprocessing_functions.mask_df(df_test)
        result = np.mean(np.where(np.isnan(masked_df_test)))

        self.assertAlmostEqual(result, 4000, delta=1) # uncertainty of +-1

    def test_mask_df_D(self):
        """One-shot test for only positive values if right length masked for mask_df-function."""
        idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
        df_test = pd.Series(0, index=idx)
        df_test.iloc[4000]= 1

        masked_df_test = preprocessing_functions.mask_df(df_test)
        result = np.where(np.isnan(masked_df_test))[0].shape[0]

        self.assertAlmostEqual(result, 1000, delta=2) # uncertainty of +-2

    def test_mask_df_E(self):
        """Test for df as input."""
        idx = pd.date_range(datetime.datetime(2000,1,1), datetime.datetime(2000,1,2), freq='1s')
        df_test = pd.DataFrame(0, index=idx, columns=['col1','col2'])

        with self.assertRaises(TypeError):
            preprocessing_functions.mask_df(df_test)

    def test_mask_df_F(self):
        """Test for pd.Series as input but no DatetimeIndex."""
        df_test = pd.Series(0,index=range(86000))

        with self.assertRaises(ValueError):
            preprocessing_functions.mask_df(df_test)

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

    # Test for read_data
    def test_read_data_A(self):
        """Smoke Test and at the same time also a one-shot test 
        tests if the columns are correct for read_data-function."""
        path_file = '../example/example_data/example_data_eruption.csv'
        df = preprocessing_functions.read_data(path_file)
        result = list(df.columns)
        self.assertListEqual(result, ['HSR', 'STD'])

    def test_read_data_B(self):
        """One-shot test to test if the columns are correct for specify the column 
        to read as a list for read_data-function."""
        path_file = '../example/example_data/example_data_eruption.csv'
        df = preprocessing_functions.read_data(path_file, ['STD'])
        result = list(df.columns)
        self.assertListEqual(result, ['STD'])

    def test_read_data_C(self):
        """One-shot test to test if the columns are correct for specify the column 
        to read as a str for read_data-function."""
        path_file = '../example/example_data/example_data_eruption.csv'
        s = preprocessing_functions.read_data(path_file, 'STD')
        df = s.to_frame()
        result = list(df.columns)
        self.assertListEqual(result, ['STD'])

    def test_read_data_D(self):
        """One-shot test to test if the columns are correct for specify the column 
        to read as a list of indeces for read_data-function."""
        path_file = '../example/example_data/example_data_eruption.csv'
        df = preprocessing_functions.read_data(path_file, [1])
        result = list(df.columns)
        self.assertListEqual(result, ['STD'])

    def test_read_data_E(self):
        """One-shot test to test if the columns are correct for specify the column 
        to read as a index for read_data-function."""
        path_file = '../example/example_data/example_data_eruption.csv'
        s = preprocessing_functions.read_data(path_file, 1)
        df = s.to_frame()
        result = list(df.columns)
        self.assertListEqual(result, ['STD'])

    def test_read_data_F(self):
        """Test for path is not a string but an integer."""
        path_file = 1
        with self.assertRaises(TypeError):
            preprocessing_functions.read_data(path_file)

    def test_read_data_G(self):
        """Test for path is not a string but a list."""
        path_file = ['This is a list']
        with self.assertRaises(TypeError):
            preprocessing_functions.read_data(path_file)

    def test_read_data_H(self):
        """Test for no column named 'time'."""
        path_file = './test_data/example_data_eruption_no_time.csv'
        with self.assertRaises(ValueError):
            preprocessing_functions.read_data(path_file)

    def test_read_data_I(self):
        """Test for 'time' does not contain strings."""
        path_file = './test_data/example_data_eruption_no_timestr.csv'
        with self.assertRaises(TypeError):
            preprocessing_functions.read_data(path_file)

    def test_read_data_J(self):
        """Test for selected column is a float."""
        path_file = '../example/example_data/example_data_eruption.csv'
        with self.assertRaises(ValueError):
            preprocessing_functions.read_data(path_file, 1.1)

    def test_read_data_K(self):
        """Test for selected column is a list of a float."""
        path_file = '../example/example_data/example_data_eruption.csv'
        with self.assertRaises(ValueError):
            preprocessing_functions.read_data(path_file, [1.1])
