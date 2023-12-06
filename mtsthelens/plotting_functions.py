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
    pygmt.makecpt(cmap="gray", series=[-1.5, 0.3, 0.01])
    fig = pygmt.Figure()
    grid = pygmt.datasets.load_earth_relief(resolution='03s', region=region)
    dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
    fig.basemap(region=region, projection=projection, frame=True)
    fig.grdimage(grid=dgrid, projection="M15c", cmap=True)
    for i in station_locations.index:
        fig.plot(
        x=station_locations.longitude[i], y=station_locations.latitude[i], style="i0.75c",
        fill=station_locations.color[i],pen="white",
        transparency=25)
    return fig

# Raw Data vs Time Stack
def plot_stack_vs_raw(stack: pd.DataFrame, raw_data:pd.DataFrame):
    n_stations = stack.shape[1]
    fig, axes = plt.subplots(nrows=n_stations, ncols=1)
    for i,col in enumerate(stack.columns):
        stack[col].plot(ax=axes[i])
        raw_data[col].plot(ax=axes[i])
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

def plot_space_stack(space_stack_attr: pd.DataFrame):
    for i, col in enumerate(space_stack_attr.columns):
        space_stack_attr.plot
    return

import pygmt

# Animations of Space Stacks with Time
def amination(stations_stack: dict = None, projection: str = "M15c"):
    # for key in stations_stack.keys()
    max_longitude = stations_stack[2005].loc['longitude'].max()
    min_longitude = stations_stack[2005].loc['longitude'].min()
    max_latitude = stations_stack[2005].loc['latitude'].max()
    min_latitude = stations_stack[2005].loc['latitude'].min()
    region = [
    round(min_longitude - .05, 2),
    round(max_longitude + .05, 2),
    round(min_latitude - .05, 2),
    round(max_latitude + .05, 2),
    ]
    pygmt.makecpt(cmap="gray", series=[-1.5, 0.3, 0.01])
    fig = pygmt.Figure()
    grid = pygmt.datasets.load_earth_relief(resolution='03s', region=region)
    dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
    fig.basemap(region=region, projection=projection, frame=True)
    fig.grdimage(grid=dgrid, projection=projection, cmap=True)
    
    colormap = "inferno"
    pygmt.makecpt(cmap=colormap, series=[0, 5])
    # pygmt.makecpt(cmap=colormap, series=[0, 5, 1])
    fig.text(x=-122.33, y=46.39, text="2022", font="22p,Helvetica-Bold,White")
    
    for key in stations_stack.keys():
        # stations = stations_stack[key].columns
        means = stations_stack[key].loc['mean']
        longitudes = stations_stack[key].loc['longitude']
        latitudes = stations_stack[key].loc['latitude']
        fig.plot(x=longitudes, y=latitudes, fill=means, cmap=True, style="i0.75c", frame=True)
    fig.colorbar(frame='af+l"DSAR"')

    fig.show()
    return 

read_dictionary = np.load('../example/example_data/stat_map.npy',allow_pickle='TRUE').item()
# print(read_dictionary)
amination(stations_stack=read_dictionary)
