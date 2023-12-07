"""
This file is for manipulation functuions for the Mt St Helens Project
"""
import numpy as np
from scipy.signal import butter, lfilter, freqz
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
sys.path.append('../CSE583_MtStHelens')

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

    for column in stack.columns:
        data = stack[column]
        filt = lowp_filter(data, cutoff, fs, order)
        filt_stack[column] = filt
          
    return filt_stack

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

"""
    For each parameter, there are two types of files, the df_stack_space and the df_yearlyParam. 
    The df_stack_space is stack(average) all the station data for each year, so there are 22 columns, and each row represents every 10 minutes of input data. 
    The df_yearlyParam is the statistical outputs, like min, max, mean, etc, of each year's data, which is from each column of the df_stack_space file. 
    Those two files help us to find potential correlations between the extrusion rate and the spatial seismic data.
"""
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
    return df_yearlyParam

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




