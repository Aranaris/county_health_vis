from urllib.request import urlopen
import shutil

with urlopen('https://data.cdc.gov/api/views/9cr5-2tt7/rows.csv?accessType=DOWNLOAD') as response, \
open('data/chd_stroke_data.csv', 'wb') as out_file:
	shutil.copyfileobj(response, out_file)
