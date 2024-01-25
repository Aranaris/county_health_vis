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

new_df = df.loc[df['Data_Value_Unit']=='per 100,000']\
	[['fips','Data_Value','LocationDesc','Year']].sort_values(by=['Year'])

years = new_df.Year.unique()
years.sort()

slider_dict = dict()
for year in years:
	slider_dict[int(year)] = {'label': year}

# initializing dash app
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
	dbc.Row([
		html.H3('Cardiovascular Disease Mortality Rate (Per 100,000)', className="text-center"),
		html.Br(),
	]),
	
	dbc.Row([
		dbc.Col([
			html.Div('Disease Type'),
			dcc.RadioItems(options=['Coronary Heart Disease', 'Stroke'], 
									value='Coronary Heart Disease',
									id='chd-disease-item'),
		]),
		
		dbc.Col([
			html.Div('Age Range'),
			dcc.RadioItems(options=[
				{'label': '35 to 64', 'value': 'Ages 35-64 years'},
				{'label': '65 and Up', 'value': 'Ages 65 years and older'},
			], value='Ages 35-64 years',
			id='chd-age-item'),
		])
		
	]),

	dbc.Row(
		dcc.Slider(1999, 2018, 1, value=1999, marks=slider_dict, id='chd-year-slider')
	),
	
	dbc.Row([
		dcc.Graph(figure={}, id='chd-graph')
	]),
	
], fluid=True)

@callback(
	Output(component_id='chd-graph', component_property='figure'),
	[Input(component_id='chd-disease-item', component_property='value'),
	Input(component_id='chd-age-item', component_property='value'),
	Input(component_id='chd-year-slider', component_property='value')]
)
def update_graph(disease_option, age_option, year_option):
	# generating figure with set parameters
	print(year_option)
	filtered_df = new_df.loc[df['Topic']==disease_option]\
		.loc[df['Stratification1']==age_option]\
		.loc[df['Year']==str(year_option)]

	fig = px.choropleth(filtered_df, geojson=counties, locations='fips', 
		color='Data_Value', 
		color_continuous_scale='Viridis',
		# animation_frame='Year',
		range_color=(0, 40),
		scope='usa',
		hover_name='LocationDesc',
		labels={'Data_Value':'Mortality Rate Per 100,000'},
		)
	fig.update_layout(
		paper_bgcolor='rgba(0,0,0,0)',
		geo_bgcolor='rgba(0,0,0,0)',
		margin={'b':0, 'l': 0}, 
		coloraxis_colorbar={
		'tickfont_color':'white',
		'title':{'text':None}, 
		'ticklabelposition':'outside bottom', 
		'len':.5, 'thickness':15, 'xpad':0
		}
		)
	
	return fig

if __name__ == '__main__':
	app.run(debug=False)
