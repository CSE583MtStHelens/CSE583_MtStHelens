# Component #1 
Name: Data Reformatter\
What it does: Makes input data readable and formatted for better readability\
Input: .csv files of the Preprocessed Time Series Data\
Output: .csv files of the Reformatted Time Series Data

# Component #2
Name: seasonalityAnalysis\
What is does: Analyses data over multiple years to find the average seasonality data, and removes the seasonality trends from the data \
Input: .csv files of the Reformatted Time Series Data\
Output: Average seasonality of each station, and the time series data with seasonality removed
