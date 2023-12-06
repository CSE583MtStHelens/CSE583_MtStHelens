# This file is for manipulation functuions for the Mt St Helens Project

import numpy as np
from scipy.signal import butter, lfilter, freqz
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal
import datetime
import glob
import math
import sys,os
sys.path.append('../CSE583_MtStHelens')
from mtsthelens import preprocessing_functions as prefcn

def filter_data(stack):

    def lowpass(cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='low', analog=False) #returns coefficients of transfer function of the low pass filter

    def lowp_filter(data, cutoff, fs, order=5):
        b, a = lowpass(cutoff, fs, order=order)
        return lfilter(b, a, data)
        
    filt_stack = stack.copy()
    order = 6
    fs = 30      #sampling rate
    cutoff = 0.02  #cutoff frequency

    b, a = lowpass(cutoff, fs, order)
    w, h = freqz(b, a, fs=fs, worN=8000) #Frequency response
    plt.plot()
    plt.plot(w, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2))
    plt.axvline(cutoff)
    plt.xlim(0, 1)
    plt.xlabel('Frequency')

    # for j in range (stack.shape[1]):
    #         data = stack[:,j]
    #         filt = lowp_filter(data, cutoff, fs, order)
    #         filt_stack[:,j] = filt

    for column in stack.columns:
        data = stack[column]
        filt = lowp_filter(data, cutoff, fs, order)
        filt_stack[column] = filt
          
    return filt_stack

"""
    In this folder are 16 outputs .csv files for each of the 8 different parameters we were trying to analyze. 
    For each parameter, there are two types of files, the df_stack_space and the df_yearlyParam. 
    The df_stack_space is stack(average) all the station data for each year, so there are 22 columns, and each row represents every 10 minutes of input data. 
    The df_yearlyParam is the statistical outputs, like min, max, mean, etc, of each year's data, which is from each column of the df_stack_space file. 
    Those two files help us to find potential correlations between the extrusion rate and the spatial seismic data.
"""
def find_max_min_within_range(df,start_index,end_index):
    # Function to find the max and min within the specified range of Dataframe
    subset = df[start_index:end_index + 1]  # Select the specified range
    max_value = subset.max()
    min_value = subset.min()
    return pd.Series({'Max_Value': max_value, 'Min_Value': min_value})

def importData_extrusion():
    '''
    Read the extrusion rate data (From sparse photograph images)
    Total volume changes(10^6 m^3)
    Total volume change rate (m^3/s)
    Extruded laca volume (10^6 m^3)
    Lava extrusion rate (m^3/s)
    Diff - the total volume changes since previous photographed date (10^6 m^3)
    '''
    print(os.getcwd())
    df_dome = pd.read_csv('example_data/dome_extrusion.txt', header=0, skiprows=0)
    df_dome.set_index('Date of photography',inplace=True)
    df_dome.index = pd.to_datetime(df_dome.index).tz_localize(None)
    df_dome['diff'] = df_dome['Total volume change(x 106 m3)']-df_dome['Total volume change(x 106 m3)'].shift(1)
    return df_dome


def importData_seismic(input_filename):
    '''
    Read all the pre-processed seismological data (there are 4 sets of data)
    df_rsam_median: Real-Time Amplitude Measurement is a measure of seismic energy
    df_zscrsam: z-score normalization is a technique that scales the\
                measurement point of a feature to have a mean of 0 and a standard deviation of 1

    df_dsar_median: Displacement Seismic Amplitude Ratio is a measure for attenuation
    df_zscdsar_median: z-score normalization. dsar normalized 

    df_rms_median: Root Mean Square is also a measure of emitted seismic energy but over the whole detectable frequency range.
    df_zscrms_median: z-score normalization. rms normalized 

    df_pga_median: Peak Ground Acceleration is giving you the\
                     maximum absolute value in the 10 minute time window after deviate the seismig ground velocity time series.
    df_zscpga_median: z-score normalization. pga normalized 
    
    '''
    #df_rsam_median = prefcn.read_data('data/'+param_name+'_extended2_long.csv')
    df_rsam_median = prefcn.read_data('example_data/'+input_filename+'.csv')
    return df_rsam_median #df_zscrsam_median, df_dsar_median, df_zscdsar_median, df_rms_median, df_zscrms_median, df_pga_median, df_zscpga_median

def stackInTime(df):
    '''
    Name: Stacking in Time\
    What it does: Analyses data over multiple years to find the average seasonality data,\
            and removes the seasonality trends from the data
    Input: pandas dataframe of the reformatted time series data\
    Output: Average seasonality of each station, data from each station with seasonality removed\
    '''
    grouped_data = df.groupby([df.index.month, df.index.day, df.index.hour, df.index.minute])
    seasonal_data = grouped_data.mean()
    seasonal_data.index = pd.to_datetime(seasonal_data.index.map(lambda x: f'2000-{x[0]:02d}-{x[1]:02d} {x[2]:02d}:{x[3]:02d}:00'))

    data_no_seasonal = df.copy()
    modified_index = pd.to_datetime(df.index.map(lambda x: f'2000-{x.month:02d}-{x.day:02d} {x.hour:02d}:{x.minute:02d}:00'))
    data_no_seasonal = data_no_seasonal - seasonal_data.loc[modified_index].values

    return seasonal_data, data_no_seasonal

# def stackInSpace(df_rsam_median):
#     '''
#     Name: Stacking in Space\
#     What it does: Analyses Data accross all stations to potential\
#                  find a correlation between the climate and the region over the years.
#     Input: .csv files of the Reformatted Time Series Data\
#     Output: Average Seasonality over all stations, stacked in time series with reasonality removed.\
#              Contains a column of maximum and minimum difference per year. Output to .csv file\
#     '''
#     min_date = df_rsam_median.index.min()
#     max_date = df_rsam_median.index.max()
#     min_year = min_date.year
#     max_year = max_date.year
#     years = range(min_year,max_year)
#     df_median_stackSpace = pd.DataFrame()
#     df_rsam_median_f = df_rsam_median.fillna(0)
#     df_median_stackSpace['df_rsam_median_SS'] = df_rsam_median_f.apply(lambda row: row[row != 0].mean(),axis = 1)

#     df_dict = {} 
#     for year in years:
#         df_year = df_median_stackSpace['df_rsam_median_SS'].loc[str(year)] # splits df into samaller df for each year
#         df_split1 = df_year[df_year.index<datetime.datetime(year,2,28,23,59,59,999)] # inclued dates until 28.2
#         df_split2 = df_year[df_year.index>datetime.datetime(year,3,1)] # includes dates from 1.3
#         df_concat = pd.concat([df_split1, df_split2]) # concat so that 29.2 removed
#         df_dict[year] = df_concat # add shorted years to dict
#     key_list = [key for key,value in df_dict.items()]
#     time_list = df_dict[2004].index.strftime('%m/%d %H:%M:%S').to_list()
#     df_stackSpace_year = pd.DataFrame(index=time_list,columns=key_list)
#     for key, value in df_dict.items():
#         df_stackSpace_year[key] = value.to_list()
#     return df_median_stackSpace, df_stackSpace_year

def df2dict(df):
    """
    Input: df along y-axis times
    Output: dict keys are years and values are 
    """
    years = np.unique(df.index.year) # extract all years from time series

    df_dict = {} 
    for year in years:
        df_year = df.loc[str(year)] # splits df into samaller df for each year
        df_split1 = df_year[df_year.index<datetime.datetime(year,2,28,23,59,59,999)] # inclued dates until 28.2
        df_split2 = df_year[df_year.index>datetime.datetime(year,3,1)] # includes dates from 1.3
        df_concat = pd.concat([df_split1, df_split2]) # concat so that 29.2 removed
        df_dict[year] = df_concat # add all stations as df, and years as keys
    return df_dict


def stackInSpace(df_rsam_median):
    '''
    Name: Stacking in Space\
    What it does: Analyses Data accross all stations to potential\
                 find a correlation between the climate and the region over the years.
    Input: .csv files of the Reformatted Time Series Data\
    Output: Average Seasonality over all stations, stacked in time series with reasonality removed.\
             Contains a column of maximum and minimum difference per year. Output to .csv file\
    '''
    df_median_stackSpace = pd.DataFrame()
    df_rsam_median_f = df_rsam_median.fillna(0)
    df_median_stackSpace['df_rsam_median_SS'] = df_rsam_median_f.apply(lambda row: row[row != 0].mean(),axis = 1)

    df_dict = df2dict(df_median_stackSpace['df_rsam_median_SS']) # brake df up into years and drop 29th feb
    
    key_list = [key for key,value in df_dict.items()]
    time_list = df_dict[2004].index.strftime('%m/%d %H:%M:%S').to_list()
    
    df_stackSpace_year = pd.DataFrame(index=time_list,columns=key_list)
    for key, value in df_dict.items():
        df_stackSpace_year[key] = value.to_list()
    return df_median_stackSpace, df_stackSpace_year

def stackSpace_yearParam(df_stackSpace_year):
    '''
     The df_yearlyParam is the statistical outputs, like min, max, mean, etc, of each year's data, which is from each column of the input dataframe. 
     '''
    df_yearlyParam = pd.DataFrame(np.nan,index=pd.Series(['max','min','mean','median']), columns=df_stackSpace_year.columns)
    for col in df_stackSpace_year.columns:
        df_yearlyParam[col].loc['max'] = df_stackSpace_year[col].max()
        df_yearlyParam[col].loc['min'] = df_stackSpace_year[col].min()
        df_yearlyParam[col].loc['mean'] = df_stackSpace_year[col].mean()
        df_yearlyParam[col].loc['median'] = df_stackSpace_year[col].median()
    # if df_stackSpace_year.columns.dtype == 'int64': # if columns are years
    #     min_year = df_stackSpace_year.columns.min()
    #     max_year = df_stackSpace_year.columns.max()
    #     years = range(min_year,max_year+1)
    #     df_yearlyParam = pd.DataFrame(np.nan,index=pd.Series(['max','min','mean','median']), columns=years)
        
    # if df_stackSpace_year.columns.dtype == 'O': # if columns are stations
    #     df_yearlyParam = pd.DataFrame(np.nan,index=pd.Series(['max','min','mean','median']), columns=df_stackSpace_year.columns)
        
    # for col in df_stackSpace_year.columns:
    #     df_yearlyParam[col].loc['max'] = df_stackSpace_year[col].max()
    #     df_yearlyParam[col].loc['min'] = df_stackSpace_year[col].min()
    #     df_yearlyParam[col].loc['mean'] = df_stackSpace_year[col].mean()
    #     df_yearlyParam[col].loc['median'] = df_stackSpace_year[col].median()
    return df_yearlyParam

def export_csv(input_filename,df):
    # Specify the path and filename for the CSV file
    print(os.getcwd())
    # Define the output directory
    output_directory = '../example/output'

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Define the file paths for CSV files
    csv_file_path = os.path.join(output_directory, input_filename + '.csv')

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=True)  





