from urllib.request import urlretrieve

urlretrieve('https://data.cdc.gov/api/views/9cr5-2tt7/rows.csv?accessType=DOWNLOAD', 'data/chd_stroke_data.csv')
    