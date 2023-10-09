import pandas as pd
from datetime import datetime, timedelta

def get_filtered_data(MAP_KEY, days_ago):
    today = datetime.today().date()
    past_date = today - timedelta(days=days_ago)
    formatted_date = past_date.strftime('%Y-%m-%d')

    # Construct the URL
    url = f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/MODIS_NRT/COD/1/{formatted_date}'
    
    # Read data from the URL
    df_cod = pd.read_csv(url)
    
    high_risk = []

    for i in range(len(df_cod)):
        if df_cod['frp'][i] > 49.1:
            extent = [
                df_cod['longitude'][i] - 0.2,
                df_cod['latitude'][i] - 0.2,
                df_cod['longitude'][i] + 0.2,
                df_cod['latitude'][i] + 0.2
            ]

            # Filter data from df_cod using the extent
            df_cod_ex = df_cod[
                (df_cod['longitude'] >= extent[0]) &
                (df_cod['latitude'] >= extent[1]) &
                (df_cod['longitude'] <= extent[2]) &
                (df_cod['latitude'] <= extent[3])
            ].copy()

            row_data = df_cod.iloc[i, :].to_dict()
            row_data['regionfire'] = len(df_cod_ex)
            high_risk.append(row_data)

    filtered_data = pd.DataFrame(high_risk)
    return filtered_data

MAP_KEY = '7fcc05b016f5f52f558080f52b4c820d'
days_ago = 5
filtered_data = get_filtered_data(MAP_KEY, days_ago)
filtered_data.to_csv('HighRiskBeforeCoordinate.csv', index=False)

def get_present(MAP_KEY, days_ago):
    today = datetime.today().date()
    past_date = today - timedelta(days=days_ago)
    formatted_date = past_date.strftime('%Y-%m-%d')

    # Construct the URL
    url = f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/MODIS_NRT/COD/1/{formatted_date}'
    
    # Read data from the URL
    df_cod = pd.read_csv(url)
    
    high_risk = []

    for i in range(len(df_cod)):
        if df_cod['frp'][i] > 49.1:
            extent = [
                df_cod['longitude'][i] - 0.2,
                df_cod['latitude'][i] - 0.2,
                df_cod['longitude'][i] + 0.2,
                df_cod['latitude'][i] + 0.2
            ]

            # Filter data from df_cod using the extent
            df_cod_ex = df_cod[
                (df_cod['longitude'] >= extent[0]) &
                (df_cod['latitude'] >= extent[1]) &
                (df_cod['longitude'] <= extent[2]) &
                (df_cod['latitude'] <= extent[3])
            ].copy()

            row_data = df_cod.iloc[i, :].to_dict()
            row_data['regionfire'] = len(df_cod_ex)
            high_risk.append(row_data)

    filtered_data = pd.DataFrame(high_risk)
    return filtered_data

days_ago = 0
present_data = get_present(MAP_KEY, days_ago)
present_data.to_csv('HighRiskCoordinate.csv', index=False)

url = 'https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=' + MAP_KEY

cod_url = 'HighRiskCoordinate.csv'
df_cod = pd.read_csv(cod_url)

df_cod_risk = pd.read_csv('HighRiskBeforeCoordinate.csv')

high_risk = []

for i in range(len(df_cod_risk)):
    old_longitude = df_cod_risk['longitude'][i]
    old_latitude = df_cod_risk['latitude'][i]
    old_regionfire = df_cod_risk['regionfire'][i]

    # Find the corresponding entries in the new DataFrame within  units of latitude and longitude
    new_entries = df_cod[
        (df_cod['longitude'] >= old_longitude - 0.2) & (df_cod['longitude'] <= old_longitude + 0.2) &
        (df_cod['latitude'] >= old_latitude - 0.2) & (df_cod['latitude'] <= old_latitude + 0.2)
    ]
    # Check for increase in regionfire for each matching entry
    for _, new_entry in new_entries.iterrows():
        new_regionfire = new_entry.get('regionfire', 0)  # Safely get 'regionfire', default to 0 if not found

        # Check if the increase in regionfire is 35 or more
        increase = new_regionfire - old_regionfire
        if increase >= 5 and new_entry.get('type', 0) == 0:
            # Append the data to the high_risk list
            high_risk.append(new_entry.to_dict())

# Create a new DataFrame from the high_risk list
high_risk_df = pd.DataFrame(high_risk)

# Save the new DataFrame to a new CSV file
high_risk_df.to_csv('HighRiskIncrease.csv', index=False)

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