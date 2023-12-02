import pandas as pd
import numpy as np
import pygmt
import matplotlib.pyplot as plt
from datetime import datetime

Mercator = "M15c"
stats = {'latitude': [46, 47],
        'longitude': [-122, -123]}
stats = pd.DataFrame(data=stats)
region = [
    stats.longitude.min() - .05,
    stats.longitude.max() + .05,
    stats.latitude.min() - .05,
    stats.latitude.max() + .05,
]
helen = (46.191, -122.196)

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

def plot_space_stack(space_stack: pd.DataFrame):
    # for i, col in enumerate(space_stack.columns):
    return

# Animations of Space Stacks with Time
def amination(region, new_stack: pd.DataFrame = None):
    fig = pygmt.Figure()
    grid = pygmt.datasets.load_earth_relief(resolution='03s', region=region)
    dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
    fig.basemap(region=region, frame=True)
    fig.grdimage(grid=dgrid, projection="M15c", cmap=True)
    lonmid = (region[0] + region[1])/2
    latmid = (region[2] + region[3])/2 - 10
    with fig.inset(position="jBR+w6.5c/6.5c+o-2.9c/-.9c"):
        fig.coast(
            projection=f"G{lonmid}/{latmid}/60/6.5c", region="g", frame="g",
            land="gray", water='white')
        # fig.plot(
        #     x=helen[1], y=helen[0], style="kvolcano/0.33c", fill="red",
        #     pen="black", projection=f"G{lonmid}/{latmid}/60/6.5c")
    return fig

amination(region=region)