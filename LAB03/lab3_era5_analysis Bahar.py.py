
# Lab 3: ERA5 Weather Data Analysis
# Nur Bahar Gürsoy
# 2022403117

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. LOAD DATA FROM FILE

def load_era5_data(file_path): # Define a function to load ERA5 CSV data and set timestamp as index
    try:
        df = pd.read_csv(file_path)  # Read CSV file into a pandas DataFrame
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None  # Return None if file does not exist
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce') 
    # Convert the 'timestamp' column to datetime objects, this allows you to perform time-based operations on the column 
    # Invalid parsing will be set as NaT (Not a Time), the code will continue
    df.set_index('timestamp', inplace=True)
    # Set 'timestamp' as the DataFrame index for time-based operations, so when you call a date from timestamp column, you get the data for the given date
    # Set 'timestamp' as index directly in the existing DataFrame (no new copy is created)
    df.sort_index(inplace=True) # Sort the DataFrame by its datetime index (chronological order)
    
    return df

berlin_file = r"C:\Users\Asus\Documents\GitHub\CE49X_Fall2025_Gursoy_Nur-Bahar\LAB03\berlin_era5_wind_20241231_20241231.csv"
munich_file = r"C:\Users\Asus\Documents\GitHub\CE49X_Fall2025_Gursoy_Nur-Bahar\LAB03\munich_era5_wind_20241231_20241231.csv"

df_berlin = load_era5_data(berlin_file) # Load Berlin ERA5 CSV data as a time-indexed DataFrame, we call the previous function
df_munich = load_era5_data(munich_file) # Load Munich ERA5 CSV data as a time-indexed DataFrame

# 2. CLEAN DATA

df_berlin.dropna(inplace=True)  # Remove rows with NaN
df_munich.dropna(inplace=True)  # Remove rows with NaN

# 3. WIND SPEED CALCULATION

def main():
    def calculate_wind_speed(u,v): 
        # u: east-west wind component (pandas Series)
        # v: north-south wind component (pandas Series)
        return np.sqrt(u**2 + v**2)

    df_berlin['wind_speed'] = calculate_wind_speed(df_berlin['u10m'], df_berlin['v10m']) 
    # Calculate wind speed for Berlin using u10m and v10m components and store as a new column
    df_munich['wind_speed'] = calculate_wind_speed(df_munich['u10m'], df_munich['v10m'])
    # Calculate wind speed for Munich using u10m and v10m components and store as a new column

# 4. TEMPORAL AGGREGATIONS (monthly wind speed avergae, seasonal wind speed average)

    def monthly_average(df: pd.DataFrame, column):
        return df.groupby(df.index.month)[column].mean()
    # Group data by month (from DatetimeIndex) and select the column, compute the mean for each month

    berlin_monthly_wind = monthly_average(df_berlin, 'wind_speed') # Calculate monthly average wind speed for Berlin and store as a pandas Series
    munich_monthly_wind = monthly_average(df_munich, 'wind_speed') # Calculate monthly average wind speed for Munich and store as a pandas Series

    def get_season(month): # this function converts a month number to a season code
    
        if month in [12, 1, 2]: # winter 
            return 1
        elif month in [3, 4, 5]: # spring
            return 2
        elif month in [6, 7, 8]: # summer
            return 3
        else:                    # autumn
            return 4

    df_berlin['season'] = df_berlin.index.month.map(get_season)
    # Convert month numbers to season codes and store in new 'season' column for Berlin
    # map() applies the get_season function to each month number
    df_munich['season'] = df_munich.index.month.map(get_season)
    #Convert month numbers to season codes and store in new 'season' column for Munich

    berlin_seasonal_wind = df_berlin.groupby('season')['wind_speed'].mean() # Group by the 'season' column and compute mean of 'wind_speed'
    munich_seasonal_wind = df_munich.groupby('season')['wind_speed'].mean()

    # 5. STATISTICAL ANALYSIS (hourly wind speed)

    df_berlin_daily = df_berlin.resample('D').mean(numeric_only=True)
    # Resample Berlin data to daily frequency and compute daily mean for numeric columns
    # Numeric_only=True ensures only numeric columns are used for mean
    df_munich_daily = df_munich.resample('D').mean(numeric_only=True)
    # Resample Munich data to daily frequency and compute daily mean for numeric columns
    # Numeric_only=True ensures only numeric columns are used for mean

    print("\n=== Top 5 Extreme Wind Speed Days (Berlin) ===")
    print(df_berlin_daily['wind_speed'].nlargest(5)) # Select the 'wind_speed' column from daily Berlin data and print the 5 largest values

    print("\n=== Top 5 Extreme Wind Speed Days (Munich) ===")
    print(df_munich_daily['wind_speed'].nlargest(5)) # Select the 'wind_speed' column from daily Munich data and print the 5 largest values
 
    df_berlin['hour'] = df_berlin.index.hour # Extract the hour (0-23) from the timestamp index and store it in a new column 'hour'
    df_munich['hour'] = df_munich.index.hour

    berlin_hourly_pattern = df_berlin.groupby('hour')['wind_speed'].mean() # Group by the 'hour' column and compute mean of 'wind_speed'
    munich_hourly_pattern = df_munich.groupby('hour')['wind_speed'].mean()


# 6. VISUALIZATIONS

    # Customize default settings for matplotlib plots (figure size, fonts, colors, etc.)
    plt.rcParams['figure.facecolor'] = 'white'  # White background for figures
    plt.rcParams['axes.facecolor']   = 'white'  # White background for axes
    plt.rcParams.update({
        'axes.grid'        : True,    # Show grid lines
        'grid.alpha'       : 0.5,     # Light grid lines
        'lines.linewidth'  : 3.0,     # Thicker lines
        'lines.markersize' : 6,       # Larger markers
        'font.size'        : 15,      # Increase default font size
    })

    # 1st Figure - Monthly Average Wind Speed

    plt.figure(figsize=(10, 6)) # Create a new figure with specified size (width=10 inches, height=6 inches)
    plt.plot(berlin_monthly_wind.index, berlin_monthly_wind.values, marker='o', label='Berlin') 
    # Plot Berlin monthly average wind speed
    # x-axis: month numbers, y-axis: average wind speed, marker='o' to show points, label for legend
    plt.plot(munich_monthly_wind.index, munich_monthly_wind.values, marker='o', label='Munich')
    plt.title("Monthly Average Wind Speed (2024)", fontsize=18, pad=10) # Set the plot title, with font size 16 and padding of 10 points above the plot
    plt.xlabel("Month", fontsize=14) # Set the label for the x-axis as "Month" with font size 14
    plt.ylabel("Wind Speed (m/s)", fontsize=14)
    plt.xticks(range(1, 13)) # Set x-axis ticks to show months from 1 to 12
    plt.legend(fontsize=12)
    plt.show()

    # 2nd Figure - Seasonal Average Wind Speed

    season_labels = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'}
    # Define a dictionary to map season codes to season names

    plt.figure(figsize=(10, 6))
    plt.bar(berlin_seasonal_wind.index - 0.15, berlin_seasonal_wind.values, width=0.3, label='Berlin')
    # Plot Berlin seasonal average wind speed as a bar chart
    # Subtract 0.15 from x positions to slightly shift bars to the left for visibility
    plt.bar(munich_seasonal_wind.index + 0.15, munich_seasonal_wind.values, width=0.3, label='Munich')
    plt.title("Seasonal Average Wind Speed (2024)", fontsize=16, pad=10)
    plt.xlabel("Season", fontsize=14)
    plt.ylabel("Wind Speed (m/s)", fontsize=14)
    plt.xticks([1, 2, 3, 4], [season_labels[s] for s in [1, 2, 3, 4]], fontsize=12)
    # Set x-axis ticks at positions 1, 2, 3, 4 and replace them with season names from season_labels dictionary
    plt.legend(fontsize=12)
    plt.show()

    # 3- Diurnal (Hourly) Pattern

    plt.figure(figsize=(10, 6))
    plt.plot(berlin_hourly_pattern.index, berlin_hourly_pattern.values, marker='o', label='Berlin')
    plt.plot(munich_hourly_pattern.index, munich_hourly_pattern.values, marker='o', label='Munich')
    plt.title("Average Diurnal (Hourly) Wind Speed", fontsize=16, pad=10)
    plt.xlabel("Hour of the Day", fontsize=14)
    plt.ylabel("Wind Speed (m/s)", fontsize=14)
    plt.xticks(range(0, 24))
    plt.legend(fontsize=12)
    plt.show()

    print("\nDone! All calculations and plots use the 'timestamp' column as DatetimeIndex.")

if __name__ == "__main__":
    main()