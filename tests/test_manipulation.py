"""
Test file for the manipulation_function.py
"""
import unittest
import sys
import os
import numpy as np
import pandas as pd

# file directory manipulation - relative import
current_directory = os.getcwd()
# Go back one folder level
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.insert(0, parent_directory)
from ..mtsthelens import manipulation_functions


# Define a class in which the tests will run
class Test_Manipulation(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        date_rng = pd.date_range(start="2022-01-01", end="2022-12-31", freq="D")
        data = {"value": np.random.rand(len(date_rng))}
        self.sample_df = pd.DataFrame(data, index=date_rng)

    def test_smoke_manipulation_A(self):
        """
        Test the two manipuation functions: stackSpace and StackSpace_yearlyParam will run
        With three stations, and start from same year as example data file
        """
        # Create a sample DataFrame for testing
        data = {
            "Station1": np.random.rand(100),
            "Station2": np.random.rand(100),
            "Station3": np.random.rand(100),
        }
        df = pd.DataFrame(
            data, index=pd.date_range("2004-01-01", periods=100, freq="D")
        )

        # smoke test whether the two functions works
        self.assertIsNotNone(manipulation_functions.stack_in_space(df))
        df_median_stackSpace, df_stackSpace_year = manipulation_functions.stack_in_space(
            df
        )
        self.assertIsNotNone(
            manipulation_functions.stack_space_year_param(df_stackSpace_year)
        )

    def test_smoke_manipulation_B(self):
        """
        Test the two manipuation functions: stackSpace and StackSpace_yearlyParam will run
        With 5 stations, and start from different year as example data file
        """
        # Create a sample DataFrame for testing
        data = {
            "Station1": np.random.rand(100),
            "Station2": np.random.rand(100),
            "Station3": np.random.rand(100),
            "Station4": np.random.rand(100),
            "Station5": np.random.rand(100),
        }
        df = pd.DataFrame(
            data, index=pd.date_range("2007-01-01", periods=100, freq="D")
        )

        # smoke test whether the two functions works
        self.assertIsNotNone(manipulation_functions.stack_in_space(df))
        df_median_stackSpace, df_stackSpace_year = manipulation_functions.stack_in_space(
            df
        )
        self.assertIsNotNone(
            manipulation_functions.stack_space_year_param(df_stackSpace_year)
        )

    def test_stackInSpace_A(self):
        """
        Test the stackInSpace function
        Created the synthetic data and test whether the funciton perform as we expected
        Test if the stackInSpace function stacks data correctly across all stations
        """
        # Create a sample DataFrame for testing
        data = {
            "Station1": np.random.rand(100),
            "Station2": np.random.rand(100),
            "Station3": np.random.rand(100),
        }
        df = pd.DataFrame(
            data, index=pd.date_range("2004-01-01", periods=100, freq="D")
        )

        # Apply the stackInSpace function
        df_median_stackSpace, df_stackSpace_year = manipulation_functions.stack_in_space(
            df
        )

        # Check if the shape of the stacked DataFrame is correct
        expected_shape = (
            99,
            1,
        )  # Stacking across all stations should result in one column
        self.assertEqual(df_median_stackSpace.shape, expected_shape)

    def test_stackInSpace_B(self):
        """
        Test the stackInSpace function
        Created the synthetic data and test whether the funciton perform as we expected
        Test if the stackInSpace function stacks data correctly across all stations
        """
        # Create a sample DataFrame for testing
        data = {
            "Station1": np.random.rand(50),
            "Station2": np.random.rand(50),
            "Station3": np.random.rand(50),
            "Station4": np.random.rand(50),
            "Station5": np.random.rand(50),
            "Station6": np.random.rand(50),
        }
        df = pd.DataFrame(data, index=pd.date_range("2009-01-01", periods=50, freq="D"))

        # Apply the stackInSpace function
        df_median_stackSpace, df_stackSpace_year = manipulation_functions.stack_in_space(
            df
        )

        # Check if the shape of the stacked DataFrame is correct
        expected_shape = (
            49,
            1,
        )  # Stacking across all stations should result in one column
        self.assertEqual(df_median_stackSpace.shape, expected_shape)

        # Check if the years in the stacked DataFrame match the input DataFrame
        self.assertListEqual(
            df_stackSpace_year.columns.to_list(),
            df_median_stackSpace.index.year.tolist()[0],
        )

    def test_stackInSpace_C(self):
        # Create a sample DataFrame for testing
        data = {
            "Station1": np.random.rand(50),
            "Station2": np.random.rand(50),
            "Station3": np.random.rand(50),
            "Station4": np.random.rand(50),
            "Station5": np.random.rand(50),
            "Station6": np.random.rand(50),
        }
        df = pd.DataFrame(data, index=pd.date_range("2009-01-01", periods=50, freq="D"))

        df_median_stackSpace, df_stackSpace_year = manipulation_functions.stack_in_space(
            df
        )
        # Test that the output DataFrames are not empty
        assert not df_median_stackSpace.empty
        assert not df_stackSpace_year.empty

    def test_stack_space_yearparam_A(self):
        """
        Test the stack_space_yearparam function
        Created the synthetic data and test whether the funciton perform as we expected
        """
        # Create a sample DataFrame for testing
        data = {
            "Station1": [10, 20, 30, 40],
            "Station2": [15, 25, 35, 45],
            "Station3": [5, 15, 25, 35],
            "Station4": [30, 40, 50, 60],
            "Station5": [30, 45, 20, 30],
        }
        df_stackSpace_year = pd.DataFrame(
            data,
            index=[
                "01/01 00:00:00",
                "01/01 01:00:00",
                "01/01 02:00:00",
                "01/01 03:00:00",
            ],
        )

        # Test if the function returns a DataFrame with the correct shape
        df_result = manipulation_functions.stack_space_year_param(df_stackSpace_year)

        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertEqual(
            df_result.shape, (4, 5)
        )  # Adjust the shape based on your expectations

        # Test if the calculated statistics are correct for each column
        expected_max = {
            "Station1": 40,
            "Station2": 45,
            "Station3": 35,
            "Station4": 60,
            "Station5": 45,
        }
        expected_min = {
            "Station1": 10,
            "Station2": 15,
            "Station3": 5,
            "Station4": 30,
            "Station5": 20,
        }
        expected_mean = {
            "Station1": 25,
            "Station2": 30,
            "Station3": 20,
            "Station4": 45,
            "Station5": 31.25,
        }
        expected_median = {
            "Station1": 25,
            "Station2": 30,
            "Station3": 20,
            "Station4": 45,
            "Station5": 30,
        }

        for col in df_stackSpace_year.columns:
            self.assertAlmostEqual(df_result[col].loc["max"], expected_max[col])
            self.assertAlmostEqual(df_result[col].loc["min"], expected_min[col])
            self.assertAlmostEqual(
                df_result[col].loc["mean"], expected_mean[col], places=3
            )
            self.assertAlmostEqual(df_result[col].loc["median"], expected_median[col])

    def test_stack_space_yearparam_B(self):
        """
        Test the stack_space_yearparam function
        Created the synthetic data and test whether the funciton perform as we expected
        """
        # Create a sample DataFrame for testing
        data = {
            "Station1": [10, 20, 30, 40],
            "Station2": [15, 25, 35, 45],
            "Station3": [5, 15, 25, 35],
        }
        df_stackSpace_year = pd.DataFrame(
            data,
            index=[
                "01/01 00:00:00",
                "01/01 01:00:00",
                "01/01 02:00:00",
                "01/01 03:00:00",
            ],
        )

        # Test if the function returns a DataFrame with the correct shape
        df_result = manipulation_functions.stack_space_year_param(df_stackSpace_year)

        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertEqual(
            df_result.shape, (4, 3)
        )  # Adjust the shape based on your expectations

        # Test if the calculated statistics are correct for each column
        expected_max = {"Station1": 40, "Station2": 45, "Station3": 35}
        expected_min = {"Station1": 10, "Station2": 15, "Station3": 5}
        expected_mean = {"Station1": 25, "Station2": 30, "Station3": 20}
        expected_median = {"Station1": 25, "Station2": 30, "Station3": 20}

        for col in df_stackSpace_year.columns:
            self.assertAlmostEqual(df_result[col].loc["max"], expected_max[col])
            self.assertAlmostEqual(df_result[col].loc["min"], expected_min[col])
            self.assertAlmostEqual(
                df_result[col].loc["mean"], expected_mean[col], places=3
            )
            self.assertAlmostEqual(df_result[col].loc["median"], expected_median[col])

    def test_yearlyParam_C(self):
        # Create a sample DataFrame for testing
        data = {
            "Station1": [10, 20, 30, 40],
            "Station2": [15, 25, 35, 45],
            "Station3": [5, 15, 25, 35],
        }
        df_stackSpace_year = pd.DataFrame(
            data,
            index=[
                "01/01 00:00:00",
                "01/01 01:00:00",
                "01/01 02:00:00",
                "01/01 03:00:00",
            ],
        )

        df_result = manipulation_functions.stack_space_year_param(df_stackSpace_year)
        # Test that the output DataFrames are not empty
        assert not df_result.empty

    def test_df2dict_returns_dict(self):
        """Smoke Test and at the same time also a one-shot test with
        a DataFrame as input and a dictionary as output for df2dict-function."""
        result = manipulation_functions.df2dict(self.sample_df)
        self.assertIsInstance(result, dict)

    def test_df2dict_returns_expected_keys(self):
        """One-shot test which compares df columns to dict keys."""
        result = manipulation_functions.df2dict(self.sample_df)
        expected_keys = self.sample_df.index.year.unique().tolist()
        self.assertListEqual(list(result.keys()), expected_keys)

    def test_df2dict_invalid_group_by_raises_error(self):
        """Test with invalide groupe passed."""
        with self.assertRaises(ValueError):
            manipulation_functions.df2dict(self.sample_df, group_by="invalid_group")

    def test_df2dict_non_datetime_index_raises_error(self):
        """Test with indeces not beeing a datetime value."""
        non_datetime_index_df = pd.DataFrame({"value": [1, 2, 3]}, index=[1, 2, 3])
        with self.assertRaises(ValueError):
            manipulation_functions.df2dict(non_datetime_index_df)

    def test_stackInSpace_handles_leap_years(self):
        leap_year_df = pd.DataFrame(
            {"value": [1, 2, 3]},
            index=pd.to_datetime(["2020-02-28", "2020-02-29", "2020-03-01"]),
        )
        result_df, _ = manipulation_functions.stack_in_space(leap_year_df)
        self.assertEqual(len(result_df), 2)

    def test_stackInTime_A(self):
        """
        Tests the stackInTime function
        Creates synthetic data and tests whether the funciton runs without errors
        Tests that the output is not empty
        """
        # Create a sample DataFrame for testing
        dates = pd.date_range(start="2001-01-01", end="2004-01-05", freq="10T")
        df = pd.DataFrame(
            {
                "Station1": np.random.randn(len(dates)),
                "Station2": 100 * np.random.randn(len(dates)) - 50,
                "Station3": np.random.randn(len(dates)),
            },
            index=dates,
        )
        df["Station3"]["2004-01-05 09:30:40"] = None

        # Test if the function runs without errors
        seasonal_data, data_no_seasonal = manipulation_functions.stack_in_time(df)

        # Test that the output DataFrames are not empty
        self.assertFalse(seasonal_data.empty)
        self.assertFalse(data_no_seasonal.empty)

    def test_stackInTime_B(self):
        """
        Tests the stackInTime function
        Creates synthetic data and tests whether the funciton runs without errors
        Tests the output types are as expected
        """
        # Create a sample DataFrame for testing
        dates = pd.date_range(start="2001-01-01", end="2004-01-05", freq="10T")
        df = pd.DataFrame(
            {
                "Station1": np.random.randn(len(dates)),
                "Station2": 100 * np.random.randn(len(dates)) - 50,
                "Station3": np.random.randn(len(dates)),
            },
            index=dates,
        )
        df["Station3"]["2004-01-05 09:30:40"] = None

        # Test if the function runs without errors
        seasonal_data, data_no_seasonal = manipulation_functions.stack_in_time(df)

        # Check if the output types are as expected
        self.assertIsInstance(seasonal_data, pd.DataFrame)
        self.assertIsInstance(data_no_seasonal, pd.DataFrame)

    def test_stackInTime_C(self):
        """
        Test the stackInTime function
        Creates synthetic data and tests whether the funciton runs without errors
        Tests for negative data, and some stations lacking all the data
        Ensures that the type and shape of the output data is as expected and that the original df is unaltered
        """
        # Create a sample DataFrame for testing
        dates = pd.date_range(start="2001-01-01", end="2004-01-05", freq="10T")
        df = pd.DataFrame(
            {
                "Station1": np.random.randn(len(dates)),
                "Station2": 100 * np.random.randn(len(dates)) - 50,
                "Station3": np.random.randn(len(dates)),
            },
            index=dates,
        )
        df["Station3"]["2004-01-05 09:30:40"] = None
        df_copy = df.copy()

        # Test if the function runs without errors
        seasonal_data, data_no_seasonal = manipulation_functions.stack_in_time(df)

        # Check if the output DataFrames have the correct shape
        self.assertEqual(
            seasonal_data.shape, (24 * 6 * 365, 3)
        )  # 24 h * 6 10-min intervals * 365 d
        self.assertEqual(data_no_seasonal.shape, df.shape)

    def test_stackInTime_D(self):
        """
        Test the stackInTime function
        Creates synthetic data and tests whether the funciton runs without errors
        Tests that the function does not manipulate the input dataframe
        """
        # Create a sample DataFrame for testing
        dates = pd.date_range(start="2001-01-01", end="2004-01-05", freq="10T")
        df = pd.DataFrame(
            {
                "Station1": np.random.randn(len(dates)),
                "Station2": 100 * np.random.randn(len(dates)) - 50,
                "Station3": np.random.randn(len(dates)),
            },
            index=dates,
        )
        df["Station3"]["2004-01-05 09:30:40"] = None
        df_copy = df.copy()

        # Test if the function runs without errors
        seasonal_data, data_no_seasonal = manipulation_functions.stack_in_time(df)

        # Check if the input DataFrame is not modified
        self.assertTrue(df.equals(df_copy))
