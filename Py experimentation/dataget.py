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

# Example usage:
MAP_KEY = '7fcc05b016f5f52f558080f52b4c820d'
days_ago = 5
filtered_data = get_filtered_data(MAP_KEY, days_ago)
filtered_data.to_csv('HighRiskBeforeCoordinate.csv', index=False)