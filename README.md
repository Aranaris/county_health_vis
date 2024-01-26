## Visualizing Heart Health Data from HealthData.gov

Taking a look at some interesting datasources provided by healthdata.gov. Currently hosted on a [Dash app via fly.io](https://health-data-vy.fly.dev/)

Rates and Trends in Coronary Heart Disease and Stroke Mortality Data Among US Adults (35+) by County – 1999-2018 [Data Source](https://healthdata.gov/dataset/Rates-and-Trends-in-Coronary-Heart-Disease-and-Str/yvac-3wdb/about_data)

Using plotly and the chloropeth tool to visualize the results in `generate_data_vis.py`

## Running the app

This is using plotly's Dash app to deploy.

Running `python generate_data_vis.py` will run a flask app locally and you can view the result in your browser.
