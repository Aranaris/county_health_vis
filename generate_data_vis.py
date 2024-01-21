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
import plotly.express as px

df = pd.read_csv('data/chd_stroke_data.csv',
                 dtype={'LocationID': str})

df['fips'] = df.apply(lambda x: locationid_to_fips(x['LocationID']), axis=1)

for year in df['Year'].unique():
   if len(year) != 4:
      continue
   else:
      new_df = df[df['Stratification1'] == 'Ages 35-64 years'][df['Topic']=='Stroke'][df['Data_Value_Unit']=='per 100,000'][df['Year']==year][['fips','Data_Value','LocationDesc']]
      fig = px.choropleth(new_df, geojson=counties, locations='fips', color='Data_Value', width=1200, height=600,
																color_continuous_scale='Viridis',
																title=f"Stroke Mortality per 100,000 ({year})",
																range_color=(0, 30),
																scope='usa',
																hover_name='LocationDesc',
																labels=dict(Data_Value='Stroke Mortality Rate Per 100,000'),
																)
      fig.update_layout(margin={'b':0, 'l': 0}, coloraxis_colorbar=dict(title=dict(text=None), ticklabelposition='outside bottom', len=.3, thickness=15, xpad=0))
			# fig.show()
      fig.write_image(f"images/StrokeMortality_{year}.png")
