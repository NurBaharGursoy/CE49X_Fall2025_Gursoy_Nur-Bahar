# CE 49X - Lab 2: Soil Test Data Analysis

# Student Name: _Nur Bahar GÜRSOY_______________  
# Student ID: __2022403117______________  
# Date: __11.10.2025______________

import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Load the soil test dataset from a CSV file.
    
    Parameters:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded DataFrame, or None if the file is not found.
    """
    # TODO: Implement data loading with error handling

    try: # Attempts to execute this block of code and catches any errors that occur
        df = pd.read_csv(file_path) # Read the CSV file and store the data as a DataFrame in the variable df
        print("Data loaded successfully.")  # Print confirmation message
        return df # Return the DataFrame
    except FileNotFoundError: # Handle the case where the specified file does not exist
        print(f"Error: File not found. Ensure the file exists at the specified path: {file_path}")
        return None # Return None if the file is not found
    except Exception as e: # Handle any other unexpected errors during file loading
        print(f"Error loading data: {e}") 
        return None # Return None if any other error occurs

def clean_data(df):
    """
    Clean the dataset by handling missing values and removing outliers from 'soil_ph'.
    
    For each column in ['soil_ph', 'nitrogen', 'phosphorus', 'moisture']:
    - Missing values are filled with the column mean.
    
    Additionally, remove outliers in 'soil_ph' that are more than 3 standard deviations from the mean.
    
    Parameters:
        df (pd.DataFrame): The raw DataFrame.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.copy() # Make a copy of the DataFrame to avoid changing the original
    
    # TODO: Fill missing values in each specified column with the column mean
    for col in ['soil_ph', 'nitrogen', 'phosphorus', 'moisture']:
        if df_cleaned[col].isnull().any(): # Check if the current column has any missing values (NaN)
            # .isnull() returns True/False for each row, and .any() checks if at least one True exists, if there is, it returns True.
            mean_val = df_cleaned[col].mean() # Calculate the mean of the column (ignoring NaNs)
            #df_cleaned[col].fillna(mean_val, inplace=True)
            df_cleaned[col] = df_cleaned[col].fillna(mean_val) #changed the code due to a warning and to remove the warning in the output
            # fillna() replaces missing (NaN) values with the mean value and assign the result back to the same column
            print(f"Filled missing values in '{col}' with mean value {mean_val:.2f}") # Print info message
    
    # TODO: Remove outliers in 'soil_ph': values more than 3 standard deviations from the mean
    ph_mean = df_cleaned['soil_ph'].mean() # Calculate mean of soil_ph column
    ph_std = df_cleaned['soil_ph'].std() # Calculate standard deviation of soil_ph
    lower_bound = ph_mean - 3 * ph_std # Define lower bound (mean - 3*std)
    upper_bound = ph_mean + 3 * ph_std # Define upper bound (mean + 3*std)
    df_cleaned = df_cleaned[(df_cleaned['soil_ph'] >= lower_bound) & (df_cleaned['soil_ph'] <= upper_bound)] 
    # Keep only rows where soil_ph is within the acceptable range (not an outlier)
    
    print(f"After cleaning, 'soil_ph' values are within the range [{lower_bound:.2f}, {upper_bound:.2f}].")
    print(df_cleaned.head()) # Display first 5 rows of cleaned data, 5 as default 
    return df_cleaned # Return the cleaned DataFrame

def compute_statistics(df, column):
    """
    Compute and print descriptive statistics for the specified column.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column (str): The name of the column for which to compute statistics.
    """
    # TODO: Calculate minimum value
    min_val = df[column].min() # Compute the smallest value in the column
    
    # TODO: Calculate maximum value
    max_val = df[column].max() # Compute the largest value in the column
    
    # TODO: Calculate mean value
    mean_val = df[column].mean() # Compute the average value
    
    # TODO: Calculate median value
    median_val = df[column].median() # Compute the median (middle value)
    
    # TODO: Calculate standard deviation
    std_val = df[column].std() # Compute how spread out the data is from the mean
    
    print(f"\nDescriptive statistics for '{column}':")
    print(f"  Minimum: {min_val}")
    print(f"  Maximum: {max_val}")
    print(f"  Mean: {mean_val:.2f}")
    print(f"  Median: {median_val:.2f}")
    print(f"  Standard Deviation: {std_val:.2f}")

def main():
    # TODO: Update the file path to point to your soil_test.csv file
    file_path = r"C:\Users\Asus\Downloads\soil_test.csv"  # The path to the CSV file containing the soil test data
    # The 'r' before the string makes it a raw string, so backslashes are treated literally
    
    # TODO: Load the dataset using the load_data function
    df = load_data(file_path) # Call the function to read data from CSV, load_data was defined at the beginning
    if df is None: # If loading failed, stop execution
        return # When used alone, 'return' immediately stops the function and does not return any value.
    
    # TODO: Clean the dataset using the clean_data function
    df_clean = clean_data(df) # Call function to clean data (handle NaN and outliers), clean_data was defined before
    
    # TODO: Compute and display statistics for the 'soil_ph' column
    compute_statistics(df_clean, 'soil_ph') # Compute stats for soil_ph, compute_statistics was defined before 
    compute_statistics(df_clean, 'nitrogen') # Compute stats for nitrogen
    compute_statistics(df_clean, 'phosphorus') # Compute stats for phosphorus
    compute_statistics(df_clean, 'moisture') # Compute stats for moisture
    
    # TODO: (Optional) Compute statistics for other columns
    # compute_statistics(df_clean, 'nitrogen')
    # compute_statistics(df_clean, 'phosphorus')
    # compute_statistics(df_clean, 'moisture')
    
if __name__ == '__main__': # Run the main function only when the script is executed directly
    # Check if this script is being run directly (not imported); if this file is imported by another script, this block will not run automatically.
    main() # Call the main() function to start the program

# =============================================================================
# REFLECTION QUESTIONS
# =============================================================================
# Answer these questions in comments below:

# 1. What was the most challenging part of this lab?
# Answer: Handling missing values and removing outliers while making sure the statistics were calculated correctly.

# 2. How could soil data analysis help civil engineers in real projects?
# Answer: Soil data analysis helps civil engineers design safe and stable foundations by understanding soil properties and behavior.

# 3. What additional features would make this soil analysis tool more useful?
# Answer: Adding data visualization, automatic outlier detection, and soil classification recommendations would make the tool more useful.

# 4. How did error handling improve the robustness of your code?
# Answer: Error handling made the code more robust by preventing crashes and managing unexpected issues gracefully.