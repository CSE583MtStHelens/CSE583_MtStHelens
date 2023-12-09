# import all packages you will need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
import datetime
import glob
import math
import sys


def calculate_distance(lat1, lat2, lon1, lon2):
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.

    Args:
        lat1 (float or int): Latitude of the first point in degrees.
        lat2 (float or int): Latitude of the second point in degrees.
        lon1 (float or int): Longitude of the first point in degrees.
        lon2 (float or int): Longitude of the second point in degrees.

    Returns:
        float: The distance between the two points in kilometers.
        
    Raises:
        TypeError if one or more of the Args is neiter an int nor a float,
    """
    if not all(isinstance(i, (int,float)) for i in [lat1, lat2, lon1, lon2]):
        raise TypeError("Input values must be an integer or float.")

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
 
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def mask_df(row):
    """
    Masks specific regions in a time series based on detected peaks.

    Args:
        row(pd.Series): A Pandas Series representing the time series data.

    Returns:
        row_masked(pd.Series): A Pandas Series with certain regions masked as NaN around detected peaks.
    
    This function identifies peaks in the input time series 'row' and masks a region around each peak by setting values to NaN. The size of the masked region is defined by subtracting 500 samples from the left base and adding 500 samples to the right base of the detected peak. If no peaks are detected, the function leaves the input time series unaltered.
    """
    peaks, properties = scipy.signal.find_peaks(row, prominence=(row.rolling('10D').median()*100).to_numpy(), distance=len(row))
    row_masked = row.copy()
    try:
#         row_masked[row_masked>min(row_masked.iloc[properties['left_bases'][0]:properties['right_bases'][0]])]=np.nan
        row_masked.iloc[properties['left_bases'][0]-500:properties['right_bases'][0]+500]=np.nan
    except:
        pass
    return row_masked

def norm(s):
    """
    Normalize a numeric array to a range between 0 and 1.

    Args:
        s(np.array or pd.Series): A numeric array or Pandas Series to be normalized.

    Returns:
        s_norm(np.array or pd.Series): A normalized version of the input array, with values between 0 and 1.
    
    This function takes a numeric array 's' and normalizes it by scaling the values within the range [0, 1]. It calculates the range of the input array by finding the difference between the maximum and minimum values. Then, it scales all values in 's' proportionally to this range, resulting in a new array 's_norm' with values between 0 (minimum) and 1 (maximum).
    """

    if not isinstance(s, (np.ndarray, pd.Series)):
        raise TypeError("Input must be a np.array or pd.Series.")
    
    if s.shape[0] == 0:
        raise ValueError("Empty np.array or pd.Series is not a valid input.")

    diff_s = max(s)-min(s)
    s_norm = ((s - min(s))/diff_s)
    return s_norm

def read_data(path_file, cols=None):
    """
    Reads data from a CSV file, converts it into a Pandas DataFrame, 
    and optionally selects specific column(s) from the DataFrame based on the 'cols' parameter.
    The time columns need to be labeld as time which will become the DataFrame index.

    Args:
        path_file (str): The path to the CSV file to be read.
        cols (str, int, list, optional): The 'cols' parameter is optional and allows you to specify which column(s) to select from the DataFrame.
            - A single column name (as a string) or column index (as an integer) to select a specific column.
            - A list of column names (as strings) or column indices (as integers) to select multiple columns.
            - If 'cols' is not specified or set to None, the entire DataFrame will be returned.

    Returns:
        pd.DataFrame or pd.Series: The function returns a Pandas DataFrame or Series containing the selected data from the CSV file. 
        The DataFrame is indexed by the 'time' column with timezone information removed.
        - If 'cols' specifies a single column, the function returns a Series.
        - If 'cols' specifies multiple columns, the function returns a DataFrame.

    Example:
        To read the entire CSV file:
        >>> df = read_data('data.csv')

        To read and select specific columns by name:
        >>> df = read_data('data.csv', cols='Column1')
        >>> df = read_data('data.csv', cols=['Column1', 'Column2'])

        To read and select specific columns by index:
        >>> df = read_data('data.csv', cols=1)
        >>> df = read_data('data.csv', cols=[0, 2, 3])
    """
    
    df = pd.read_csv(path_file)
    df.set_index('time', inplace=True)
    df.index = pd.to_datetime(df.index).tz_localize(None)

    if cols is not None:
        if isinstance(cols, str):
            df = df[cols]
        elif isinstance(cols, int):
            df = df.iloc[:, cols]
        elif isinstance(cols, float):
            raise ValueError("Column should be a string or integer or a list of eighter stings or integers.")
        elif isinstance(cols, list):
            if not (all(isinstance(col, (int)) for col in cols) or all(isinstance(col, (str)) for col in cols)):
                raise ValueError("Column list should only contain strings or integers.")
            if all(isinstance(col, int) for col in cols):
                df = df.iloc[:, cols]
            elif all(isinstance(col, str) for col in cols):
                df = df[cols]

    return df
