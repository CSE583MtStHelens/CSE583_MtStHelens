import unittest
import numpy as np
import pandas as pd
import sys, os

#file directory preprocessing - relative import
current_directory = os.getcwd()
# Go back one folder level
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.insert(0, parent_directory)
from mtsthelens import preprocessing_functions

#This script includes 8 test to test the knn_regression function.
# To run the test navigate into the directory hw3-koepflma
# You can eighter type 'python -m unittest discover' or specify the folder with 'python -m unittest discover -s tests'

# Define a class in which the tests will run
class TestPreprocessingFunctions(unittest.TestCase):


    # def test_calculate_distance(lat1, lat2, lon1, lon2):
        
    #     return False
    
    # def test_mask_df(row):
        
    #     return False
    
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
    
    # def test_read_data(path_file, cols=None):
    
    #     return False
