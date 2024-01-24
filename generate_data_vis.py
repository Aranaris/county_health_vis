import json
from urllib.request import urlopen

import pandas as pd
import plotly.express as px

# get GeoJSON data for county map
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	counties = json.load(response)

# reading source csv and updating locationid to be compatible with fips
def locationid_to_fips(locationid):
	if len(str(locationid)) < 5:
		return f'0{locationid}'
	else:
		return f'{locationid}'

df = pd.read_csv('data/chd_stroke_data.csv',
	dtype={'LocationID': str}, low_memory=False)

df['fips'] = df.apply(lambda x: locationid_to_fips(x['LocationID']), axis=1)

# filtering down dataframe for generating a meaningful graph for each year
# key parameters are age group stratification, stroke vs chd, and per 100,000 unit

new_df = df.loc[df['Stratification1'] == 'Ages 35-64 years']\
	.loc[df['Topic']=='Stroke']\
	.loc[df['Data_Value_Unit']=='per 100,000']\
	[['fips','Data_Value','LocationDesc','Year']].sort_values(by=['Year'])

# generating figure with set parameters

fig = px.choropleth(new_df, geojson=counties, locations='fips', 
	color='Data_Value', 
	width=1200, height=600,
	color_continuous_scale='Viridis',
	title='Stroke Mortality per 100,000',
	animation_frame='Year',
	range_color=(0, 40),
	scope='usa',
	hover_name='LocationDesc',
	labels={'Data_Value':'Stroke Mortality Rate Per 100,000'},
	)
fig.update_layout(margin={'b':0, 'l': 0}, coloraxis_colorbar={'title':{'text':None}, 
	'ticklabelposition':'outside bottom', 'len':.5, 'thickness':15, 'xpad':0})
# fig.show()

# initializing dash app
from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div([
	html.Div(children='First Dash App'),
	dcc.Graph(figure=fig)
])

if __name__ == '__main__':
	app.run(debug=True)
