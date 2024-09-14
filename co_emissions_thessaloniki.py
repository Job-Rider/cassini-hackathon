import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

# Open the NetCDF file
ds = xr.open_dataset('dataset.nc')

# Specify the region and time range:
lat_min, lat_max = 40.50, 40.75  # Latitude range for Thessaloniki, Greece
lon_min, lon_max = 22.75, 23  # Longitude range for Thessaloniki, Greece
time_start, time_end = '2023-12-03', '2023-12-10'  # Time range

# Slice the dataset by latitude, longitude, and time
co_sliced = ds['co'].sel(
    lat=slice(lat_min, lat_max),
    lon=slice(lon_min, lon_max),
    time=slice(time_start, time_end)
)

# Convert the sliced data to a pandas DataFrame
df = co_sliced.to_dataframe().reset_index()

# Filter to keep only relevant columns: time, lat, lon, and CO
df_filtered = df[['time', 'lat', 'lon', 'co']]

# Convert 'time' to a more readable format with the day of the week
df_filtered['time'] = pd.to_datetime(df_filtered['time'])

# Group by 'time' and calculate the mean CO for each time step
df_avg = df_filtered.groupby('time').mean().reset_index()

# Apply a rolling average to smooth the trend
window_size = 20  # You can adjust the window size for smoother/less smooth trends
df_avg['trend'] = df_avg['co'].rolling(window=window_size, min_periods=1).mean()

# Prepare x-axis labels: show the day of the week only once per day
time_labels = df_avg['time'].dt.strftime('%A')  # Get the day of the week
time_labels_unique = []  # Create a list to hold labels

# Loop through the time labels and add a label only for the first instance of each day
previous_day = ''
for label in time_labels:
    if label != previous_day:
        time_labels_unique.append(label)
        previous_day = label
    else:
        time_labels_unique.append('')  # Add an empty label for non-unique days

# Plotting the data and the trend line
plt.figure(figsize=(10, 6))

# Plot trend (rolling average)
plt.plot(df_avg['time'], df_avg['trend'], color='r', linestyle='--', label='Trend (Rolling Avg)', linewidth=2)

# Apply the custom labels to the x-axis
plt.xticks(df_avg['time'], labels=time_labels_unique, rotation=45)

# Formatting the plot
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Mean CO Concentration', fontsize=12)
plt.title('Mean CO Concentration with Trend in Thessaloniki (Dec 3-10, 2023)', fontsize=14)
plt.grid(True)
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()

# Save to a CSV file
current_timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
df_filtered.to_csv('co_thessaloniki_.csv', index=False)
df_avg.to_csv('co_avg_thessaloniki_.csv', index=False)

# Close the dataset
ds.close()

print("CSV files created: co_thessaloniki_" + current_timestamp + ".csv and co_avg_thessaloniki_" + current_timestamp + ".csv")
