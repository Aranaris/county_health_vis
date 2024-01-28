import json
import math
from urllib.request import urlopen

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

# get GeoJSON data for county map
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	counties = json.load(response)

# reading source csv and updating locationid to be compatible with fips
def locationid_to_fips(locationid):
	if len(str(locationid)) < 5:
		return f'0{locationid}'
	else:
		return f'{locationid}'

with urlopen('https://data.cdc.gov/api/views/9cr5-2tt7/rows.csv?accessType=DOWNLOAD') as file:
	df = pd.read_csv(file,
		dtype={'LocationID': str}, low_memory=False)

df['fips'] = df.apply(lambda x: locationid_to_fips(x['LocationID']), axis=1)

# filtering down dataframe for generating a meaningful graph for each year
# key parameters are age group stratification, stroke vs chd, and per 100,000 unit

new_df = df.loc[df['Data_Value_Unit']=='per 100,000']\
	[['fips','Data_Value','LocationDesc','Year']].sort_values(by=['Year'])

#setting up the year column for slider 
years = new_df.Year.unique()
years.sort()
slider_dict = {
	int(years[0]): {'label': years[0]},
	int(years[-1]): {'label': years[-1]},
}

# initializing dash app
external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = dbc.Container([
	dbc.Row([
		dbc.Col(
			html.H4('Cardiovascular Disease Mortality Rate (Per 100,000)', className='text-center'),
			width={'size': 8, 'offset': 2}
		),
		html.Br(),
	],
	),
	
	dbc.Row([
		dbc.Col([
			html.H6('Disease Type'),
			dcc.RadioItems(
									options=[
										{'label': 'Coronary (CHD)', 'value': 'Coronary Heart Disease'},
										{'label': 'Stroke', 'value':'Stroke'},
										], 
									value='Coronary Heart Disease',
									id='chd-disease-item',
									style={'font-size': 12}),
		], width={'size': 4, 'offset': 1}),
		
		dbc.Col([
			html.H6('Age Range'),
			dcc.RadioItems(options=[
				{'label': '35 to 64', 'value': 'Ages 35-64 years'},
				{'label': '65 and Up', 'value': 'Ages 65 years and older'},
			], value='Ages 35-64 years',
			id='chd-age-item',
			style={'font-size': 12}),
		], width={'size': 4, 'offset': 2}),
	],
	className='g-0'
	),

	dbc.Row([
		html.Br()
	]),

	dbc.Row([
			dbc.Col(
				dcc.Slider(1999, 2018, 1, value=2018, 
										marks=slider_dict,
										included=False,
										tooltip={"placement": "bottom", "always_visible": True},
										id='chd-year-slider'),	
				align='center',
				width={'size': 10, 'offset': 1}
			)
			
		],
	),
	
	dbc.Row([
		dbc.Col(
			dcc.Loading(
				id='chd-graph-loading',
				type='default',
				children=dcc.Graph(figure={}, id='chd-graph'),
			),
			align='end'
		),
	]),
	
], fluid=True)

@callback(
	Output(component_id='chd-graph', component_property='figure'),
	[Input(component_id='chd-disease-item', component_property='value'),
	Input(component_id='chd-age-item', component_property='value'),
	Input(component_id='chd-year-slider', component_property='value')],
)
def update_graph(disease_option, age_option, year_option):
	# generating figure with set parameters
	filtered_df = new_df.loc[df['Topic']==disease_option]\
		.loc[df['Stratification1']==age_option]\
		.loc[df['Year']==str(year_option)]
	
	upper_quantile = filtered_df['Data_Value'].quantile(.75)
	upper_bar_range = int(math.ceil(upper_quantile / 40.0)) * 40

	fig = px.choropleth(filtered_df, geojson=counties, locations='fips', 
		color='Data_Value', 
		color_continuous_scale='Viridis',
		range_color=(0, upper_bar_range),
		scope='usa',
		hover_name='LocationDesc',
		labels={'Data_Value':'Mortality Rate Per 100,000'},
		)
	fig.update_layout(
		paper_bgcolor='rgba(0,0,0,0)',
		geo_bgcolor='rgba(0,0,0,0)',
		margin={'b':0, 'l': 0, 't': 0, 'r': 20}, 
		coloraxis_colorbar={
		'tickfont_color':'white',
		'title':{'text':None}, 
		'ticklabelposition':'outside bottom', 
		'len':.5, 'thickness':15, 'xpad':0,
		'x':.92,
		'tickfont_size': 8
		},
		)
	
	return fig

if __name__ == '__main__':
	app.run(debug=False)
