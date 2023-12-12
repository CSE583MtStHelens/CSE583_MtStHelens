# Component specification of the MtStHelens from SeismoMech
Team: Yash Bhangale, Shreeya Gadgil, Manuela Köpfli, Callum Keddie, Guiliang Zheng
Course Project: CSE 583 | Team Repo: https://github.com/CSE583MtStHelens/CSE583_MtStHelens

# Software components
## example_tutorial
The example tutorial is a Jupyter Notebook file to demonstrate how the software works, and how to use each of our functions to apply the new seismic data from seismologists with the tool. A small-size synthetic data with the same data structure was created for computational efficiency. Once the user understands the utility of each function, a large set of raw seismic data collected from seismic stations around the volcano could be applied by this tool to generate visual plots indicating correlations between seismic activities and volcanic activities.

## test functions
Three test modules were generated according to the intended functionality of the software to test out the validity of each function. For each function written in the module, at least four test cases were written to make sure it worked as expected.

## main functions (MtStHelens)
Three modules were written for different data manipulation purposes: data processing, data manipulation, and data plotting. This is the main body of the software tool we developed. The purpose of this software is to generate straightforward visual plots from raw seismic data indicating important correlations to seismic researchers. 

## manipulation functions -- main function
### Component #1
Name: Filter Data\
What it does: Act as a low pass filter to filter out the high-frequency noise of the given data.\ The high-frequency noise is typically seen from the seismic data, which makes plots messy and\
hard to visualize the underlying.\
Input: data frame of any pre-processed data.\
Output: The data frame filtered out the high-frequency noise from the original data set.

### Component #2
Name: Stacking in Time\
What it does: Analyses data over multiple years to find the average seasonality data,\
            and removes the seasonality trends from the data.
Input: pandas data frame of the reformatted time series data.\
Output: Average seasonality of each station, data from each station with seasonality removed.

### Component #3
Name: Stacking in Space\
What it does: Analyses Data across all stations to potential\
                find a correlation between the climate and the region over the years.
Input: .csv files of the Reformatted Time Series Data\
Output: Average Seasonality over all stations, stacked in time series with seasonality removed.\
        Contains a column of maximum and minimum difference per year. Output to .csv file

### Component #4
Name: Stacking in Space with yearly statistic parameters\
What it does: Generate statistic parameters like min, max, mean, and median for \
each year's stack in space seismic data.\
Input: Dataframe of the stack in space.\
Output: Dataframe of statistic parameters in index and years as column, generated\
from the stack in the space data frame.

### Component #5
Name: data frame to dictionary\
What it does: Group a data frame or time series by year, month, or day based on the DatetimeIndex.\
Input: df (pd.DataFrame or pd. Series): The input DataFrame or time series with a DatetimeIndex.\
        group_by (str, optional): The time unit to group by. \
        Accepted values are 'year', 'month', or 'day'. Defaults to 'year'.\
Output: Dict: A dictionary where keys are years, months, or days,\
                 and values are corresponding data frames or time series.

## plotting function -- main function
### Component #1
Name: plot stack vs raw\
What it does: Group a data frame or time series by year, month, or day based on the DatetimeIndex.\
Input: df (pd.DataFrame or pd. Series): The input DataFrame or time series with a DatetimeIndex.\
        group_by (str, optional): The time unit to group by. \
        Accepted values are 'year', 'month', or 'day'. Defaults to 'year'.\
Output: Dict: A dictionary where keys are years, months, or days,\
                 and values are corresponding data frames or time series.

## preprocessing function -- main function
### Component #1
Name: calculate distance\
What it does: Calculate the distance between two points\
                on the Earth's surface using the Haversine formula.\
Input:  lat1 (float or int): Latitude of the first point in degrees.\
        lat2 (float or int): Latitude of the second point in degrees.\
        lon1 (float or int): Longitude of the first point in degrees.\
        lon2 (float or int): Longitude of the second point in degrees.\
Output: float: The distance between the two points in kilometers.\

### Component #2
Name: mask data frame\
What it does: Masks specific regions in a time series based on detected peaks.\
Input: row(pd. Series): A Pandas Series representing the time series data.\
Output: row_masked(pd. Series): A Pandas Series with certain regions masked as NaN
                                around detected peaks.

### Component #3
Name: normalization\
What it does: Normalize a numeric array to a range between 0 and 1.\
    This function takes a numeric array 's' and normalizes it by scaling the values
    within the range [0, 1]. It calculates the range of the input array by finding the
    difference between the maximum and minimum values. Then, it scales all values in 's'
    proportionally to this range, resulting in a new array 's_norm' with values 
    between 0 (minimum) and 1 (maximum).\
Input: s(np. array or pd. Series): A numeric array or Pandas Series to be normalized.\
Output: s_norm(np. array or pd. Series): A normalized version of the input array, 
                                        with values between 0 and 1.
### Component #4
Name: read \
What it does: Group a data frame or time series by year, month, or day based on the DatetimeIndex.\
Input: path_file (str): The path to the CSV file to be read.\
        cols (str, int, list, optional): The 'cols' parameter is optional and allows you to specify 
        which column(s) to select from the DataFrame.\
            - A single column name (as str) or column index (as int) to select a specific column.\
            - A list of column names (as str) or column indices (as int) to select multiple columns.\
            - If 'cols' is not specified or set to None, the entire DataFrame will be returned.\
Output: pd.DataFrame or pd.Series: The function returns a Pandas DataFrame or Series 
        containing the selected data from the CSV file.\
        The DataFrame is indexed by the 'time' column with timezone information removed.\
        - If 'cols' specifies a single column, the function returns a Series.\
        - If 'cols' specifies multiple columns, the function returns a DataFrame.

# Interactions to accomplish use cases
For the use case 1 described in the functional specifications, where a seismic researcher tries to find out the correlations between the seismic attenuation and the magma extrusion rate during the eruption of a volcano， the researcher would first pre-process their collected data using our pre-processing function to the specific format the rest of the code need. They would then, use the manipulation function to manipulate the data, either stack the data in time to find the trend with seasonality removed or stack in space to find the correlation between the climate and the region seismic activity of the region over the year. They would use those data to generate the plot using our plotting function to visualize the data and find the correlation between the seismic data and the factors they are interested in. \

In order for the user to fully understand how our code works, we wrote an example tutorial explaining how each function works using small synthetic data. The researcher would first go through the tutorial to fully understand our code before they apply the tool to their raw data. 

# Preliminary plan
 - Collect the seismic data from open web data sources, which contain the seismic statistic data of MtStHelens from different seismic stations across             the region over the past 22 years.\
 - Create a set of synthetic data based on the large data sets collected with the same data structure as the test data set to validate the                         functionality of the software and for demonstration purposes.\
 - Write the test cases according to the intended purpose of the software.\
 - Write the three main modules for the different general purposes of the tool: data preprocessing, data manipulation, and data plotting for                         visualization.\
 - Test the validity of the software and pass all the test cases.\
 - Write a demonstration tutorial to show how to use the software for the users.\
 - Generate the setup.py file to make software runnable independent from the devices, and the environment.yml file to make the user know what type of             standard modules were used in the software.\
 - Write thorough documentation and clean up the code to make the software readable and understandable.\
