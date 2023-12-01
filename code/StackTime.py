import pandas as pd
import matplotlib.pyplot as plt

def average_seasonal_data(df, column_name):
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute

    # Group by year, month, day, hour, and minute, calculate the mean for each group
    avg_data = df.groupby(['year', 'month', 'day', 'hour', 'minute'])[column_name].mean().reset_index()
    avg_data['datetime'] = pd.to_datetime(avg_data[['year', 'month', 'day', 'hour', 'minute']])
    avg_data = avg_data[['datetime', column_name]]

    return avg_data

# Example usage:
df = pd.read_csv('your_data.csv') 
avg_seasonal_data = average_seasonal_data(df,'column_name')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(avg_seasonal_data['datetime'], avg_seasonal_data['sensor_data'])
plt.title('Average Seasonal Data Over a Day')
plt.xlabel('Datetime')
plt.ylabel('Sensor Data')
plt.grid(True)
plt.show()