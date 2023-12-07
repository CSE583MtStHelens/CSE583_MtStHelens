import pandas as pd
import numpy as np
import pygmt
import matplotlib.pyplot as plt
from datetime import datetime
import sys,os

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

def plot_space_stack(yearly_params: pd.DataFrame):
    fig = plt.figure()
    plt.plot(yearly_params.columns, yearly_params.loc['mean'], marker='.')
    plt.plot(yearly_params.columns, yearly_params.loc['min'], marker='*')
    plt.plot(yearly_params.columns, yearly_params.loc['max'], marker='x')
    plt.plot(yearly_params.columns, yearly_params.loc['median'], marker='o')
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




# Animations
def MinMax4plotting(read_dictionary: dict = None):
    """
    Compute the minimum and maximum values for each row in a dictionary of DataFrames.

    Args:
        read_dictionary (dict): A dictionary where keys are DataFrame names and values are DataFrames.

    Returns:
        tuple: Two DataFrames, the first containing the minimum values per row, and the second containing the maximum values.

    Raises:
        ValueError: If the input dictionary is empty.
        TypeError: If the input is not a dictionary or if the values in the dictionary are not DataFrames.
    """
    # Check if the input is a dictionary
    if not isinstance(read_dictionary, dict):
        raise TypeError("Input must be a dictionary.")

    # Check if the dictionary is empty
    if not read_dictionary:
        raise ValueError("Input dictionary is empty.")

    # Initialize lists to store min and max values for each row
    min_values_per_row = []
    max_values_per_row = []

    # Loop through the DataFrames in the dictionary
    for key, df in read_dictionary.items():
        # Check if the values are DataFrames
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Value associated with key '{key}' is not a DataFrame.")

        # Get the min and max values for each row
        min_values = df.min(axis=1)
        max_values = df.max(axis=1)

        # Append the min and max values to the lists
        min_values_per_row.append(min_values)
        max_values_per_row.append(max_values)

    # Convert the lists to DataFrames
    min_df = pd.DataFrame(min_values_per_row, index=read_dictionary.keys()).transpose()
    max_df = pd.DataFrame(max_values_per_row, index=read_dictionary.keys()).transpose()

    return min_df, max_df


def map_plot(df: pd.DataFrame = None,
             color_min_max: list = None,
             colormap: str = None, 
             parameter: str = None,
             key: str = None,
             region: list = None,
             projection: str = "M15c"):
    # load base map and transfer to hillshade
    pygmt.makecpt(cmap="gray", series=[-1.5, 0.3, 0.01])
    fig = pygmt.Figure()
    grid = pygmt.datasets.load_earth_relief(resolution='03s', region=region)
    dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
    fig.basemap(region=region, projection=projection, frame= [f"+t{key}"])
    fig.grdimage(grid=dgrid, projection=projection, cmap=True)
    # Plot markers using latitude and longitudes
    pygmt.makecpt(cmap=colormap, series=color_min_max)    
    means = df.loc['mean']
    longitudes = df.loc['longitude']
    latitudes = df.loc['latitude']
    fig.plot(x=longitudes, y=latitudes, fill=means,
              cmap=True, style="i0.75c", frame=True)
    fig.colorbar(frame='af+l"DSAR"')
    output_directory = './output/plot/animation/{}'.format(parameter)
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    fig.savefig(output_directory + f'{parameter}_{key}.png')
    return

#bjbfwhfijnihf
def animation(read_dictionary: dict = None, parameter: str = None, colormap: str = None):
    min_df, max_df = MinMax4plotting(read_dictionary)
    df_min_max = pd.DataFrame(columns=['minimum','maximum'])
    df_min_max['minimum'] = min_df.min(axis=1)
    df_min_max['maximum'] = max_df.max(axis=1)

    region = [
    round(df_min_max['minimum'].loc['longitude'] - .05, 2),
    round(df_min_max['maximum'].loc['longitude'] + .05, 2),
    round(df_min_max['minimum'].loc['latitude'] - .05, 2),
    round(df_min_max['maximum'].loc['latitude'] + .05, 2),
    ]
 
    color_min_max = [int(df_min_max['minimum'].loc[parameter]), int(df_min_max['maximum'].loc[parameter])]

    for key, value in read_dictionary.items():

        map_plot(value, color_min_max, colormap, parameter, key, region)

    return
