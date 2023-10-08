import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('HighRiskIncrease.csv')

# Convert 'acq_time' to a datetime format
df['acq_time'] = pd.to_datetime(df['acq_time'], format='%H%M')

# Sort the DataFrame by 'acq_time' in descending order
df.sort_values(by=['latitude', 'longitude', 'acq_time'], ascending=[True, True, False], inplace=True)

# Keep only the first row for each unique latitude and longitude combination
filtered_df = df.drop_duplicates(subset=['latitude', 'longitude'], keep='first')

# Reset the index of the resulting DataFrame
filtered_df.reset_index(drop=True, inplace=True)

# Convert 'acq_time' back to the original format (HHMM)
filtered_df.loc[:, 'acq_time'] = filtered_df['acq_time'].dt.strftime('%H%M')

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_output.csv', index=False)