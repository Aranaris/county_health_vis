from urllib.request import urlopen

with urlopen('https://data.cdc.gov/api/views/9cr5-2tt7/rows.csv?accessType=DOWNLOAD') as response, \
open('data/chd_stroke_data.csv', 'wb') as out_file:
	data = response.read()
	out_file.write(data)
