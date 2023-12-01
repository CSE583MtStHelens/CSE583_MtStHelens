import pandas as pd
import numpy as np
import pygmt
import matplotlib.pyplot as plt
from datetime import datetime

Mercator = "M15c"
# Stations Map using PyGMT
def plot_stations_map(
        region,
        station_locations = None,
        projection = Mercator):
    fig = pygmt.Figure()
    fig.basemap(region=region, projection=projection, frame=True)
    for i in station_locations.index:
        fig.plot(
        x=station_locations.longitude[i], y=station_locations.latitude[i], style="i0.75c",
        pen="white",
        transparency=25)
        fig.colorbar(cax=station_locations.elevation)
    return fig

# Raw Data vs Time Stack
def plot_time_stack(time_stack: pd.DataFrame):
    n_stations = time_stack.shape[1]-1
    fig, axes = plt.subplots(nrows=n_stations, ncols=1)
    for i,col in enumerate(time_stack.columns):
        time_stack[col].plot(ax=axes[i])
    return fig

# Raw Data vs Filtered Stack
def plot_filtered_stack(filtered_stack: pd.DataFrame):
    n_stations = filtered_stack.shape[1]-1
    fig, axes = plt.subplots(nrows=n_stations, ncols=1)
    for i,col in enumerate(filtered_stack.columns):
        filtered_stack[col].plot(ax=axes[i])
    return fig


# Extrusion Rate
def plot_extrusion(extrusion_data: pd.DataFrame,
                        raw_data: pd.DataFrame,
                        time_stack: pd.DataFrame = None,
                        filtered_stack: pd.DataFrame = None):
    """
    Plots and compares extrusion rate with the raw DSAR, time stacked DSAR and Filtered DSAR.
    extrusion_data: Contains Date of Photography, Total Volume Change,
    Total Volume Change Rate, Extruded Lava Volume and Lava Extrusion Rate
    raw_data: Contains time, and readings for stations
    time_stack:
    filtered_stack:
    Returns an image that compares extrusion rate with DSAR values for raw data, 
    time stacked data and filtered data
    """
    min_date = extrusion_data.index.min()
    max_date = extrusion_data.index.max()
    n_stations = raw_data.shape[1]-1
    raw_data = raw_data.loc[min_date:max_date]
    time_stack = time_stack.loc[min_date:max_date]
    filtered_stack = filtered_stack.loc[min_date:max_date]
    vol_change_rate = extrusion_data.columns[1]
    lava_ext_rate = extrusion_data.columns[3]
    fig, axes = plt.subplots(nrows=n_stations, ncols=1)
    for i, col in enumerate(raw_data.columns):
        raw_data[col].plot(ax=axes[i])
        time_stack[col].plot(ax=axes[i])
        filtered_stack[col].plot(ax=axes[i])
        extrusion_data[vol_change_rate].plot(ax=axes[i])
        extrusion_data[lava_ext_rate].plot(ax=axes[i])
    return fig


# Animations of Space Stacks with Time
def amination(n_years, space_stack: pd.DataFrame):
    return
