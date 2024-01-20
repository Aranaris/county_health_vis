# from urllib.request import urlopen
# import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

import pandas as pd
df = pd.read_csv('data/chd_stroke_data.csv')
print(df.head(5))

new_df = df[df['Stratification1'] == 'Ages 35-64 years'][df['Topic']=='Stroke'][['LocationID','Data_Value']]
print(new_df.head(5))
