# Component #0 
Name: Data Reformatting\
What it does: Makes input data readable and formatted for better readability\
Input: .csv files of the Preprocessed Time Series Data\
Output: df of the Reformatted Time Series Data

# Component #1 
Name: Data Smoothing\
What it does: Removes outlier and apply some smoothing (in time)\
Input: .csv files of the Reformatted Time Series Data\
Output: df of the Smoothed Time Series Data

# Component #2
Name: Seasonality Analysis\
What is does: Analyses data over multiple years to find the average seasonality data, \
                and removes the seasonality trends from the data \
Input: .csv files of the Reformatted Time Series Data\
Output: Average seasonality of each station, and the time series data with seasonality removed. Output to .csv file

# Component #3
Name: Stacking in Space\
What it does: Analyses Data accross all stations to potential find a correlation\
                between the climate and the region over the years.
Input: .csv files of the Reformatted Time Series Data\
Output: Average Seasonality over all stations, stacked in time series with reasonality removed.\
        Contains a column of maximum and minimum difference per year. Output to .csv file\

# Component #4
Name: Filtering\
What it does: Take data over the time series data, applies a high pass filter and lowpass filters and removes disturbances.\
Input: .csv files of the Reformatted Time Series Data.\
Output: Outputs disturbances using the high pass filter. Smoothens data using the low pass filter. Outputs to a .csv file.\

# Component #5
Name: Map Figures\
What it does: Visualization of the spatial data.\
Input: Station Coordinates, Amplitude Differences.\
Output: Figure showing aplitude differences in space.\

# Component #6
Name: Data Manipulation Quality Control.\
What it does: Visualization and Comparison of Time Stack and Filtered Data with Raw Data.\
Input: Time Stack Data, Filtered Data and Raw Data.\
Output:	Figures showing subplots of different stations in a time series.\

# Component #7
Name: Change of Readings with Time (Animation).\
What it does: Visualization and study of change in readings averaged for all stations over the years.\
Input: Space Stack Data, Raw Data.\
Output: Figures with subplots of average data of all stations over the years.\
