import pandas as pd

MAP_KEY = '7fcc05b016f5f52f558080f52b4c820d'

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
        if increase >= 10 and new_entry.get('type', 0) == 0:
            # Append the data to the high_risk list
            high_risk.append(new_entry.to_dict())

# Create a new DataFrame from the high_risk list
high_risk_df = pd.DataFrame(high_risk)

# Save the new DataFrame to a new CSV file
high_risk_df.to_csv('HighRiskIncrease.csv', index=False)