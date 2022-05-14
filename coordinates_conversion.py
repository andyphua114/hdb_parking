import pandas as pd
import json
import requests

#load the original dataset from gov.sg
#https://data.gov.sg/dataset/hdb-carpark-information
hdb_carpark = pd.read_csv('hdb-carpark-information.csv')

#convert the x, y coordinates from float to string
hdb_carpark['x_coord'] = hdb_carpark['x_coord'].astype(str)
hdb_carpark['y_coord'] = hdb_carpark['y_coord'].astype(str)

#iterrate through the rows to convert the x, y coordinates from 3414(SVY21) to 4326(WGS84) format
#using the coordinates converters API from onemap.gpv.sg
for index, row in hdb_carpark.iterrows():
    x = row['x_coord']
    y = row['y_coord']
    response = requests.get('https://developers.onemap.sg/commonapi/convert/3414to4326?X=' + x + '&Y=' + y)
    coord = response.json()
    hdb_carpark.loc[index,'lat'] = coord['latitude']
    hdb_carpark.loc[index,'lon'] = coord['longitude']

#export to a new csv file
hdb_carpark.to_csv('hdb-carpark-lat-lon.csv')

