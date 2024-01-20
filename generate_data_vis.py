from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

def locationid_to_fips(locationid):
    if len(str(locationid)) < 5:
      return f'0{locationid}'
    else:
      return f'{locationid}'

import pandas as pd
df = pd.read_csv('data/chd_stroke_data.csv',
                 dtype={'LocationID': str})

df['fips'] = df.apply(lambda x: locationid_to_fips(x['LocationID']), axis=1)

new_df = df[df['Stratification1'] == 'Ages 35-64 years'][df['Topic']=='Stroke'][df['Data_Value_Unit']=='per 100,000'][df['Year']=='2018'][['fips','Data_Value','LocationDesc']]

import plotly.express as px

fig = px.choropleth(new_df, geojson=counties, locations='fips', color='Data_Value',
                           color_continuous_scale='Viridis',
                           range_color=(0, 40),
                           scope='usa',
                           hover_name='LocationDesc',
                           labels=dict(Data_Value='Stroke Mortality Rate Per 100,000')
                          )
fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
fig.show()
