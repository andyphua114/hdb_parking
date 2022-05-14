from dataclasses import dataclass
import pandas as pd
import json
import requests
import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk
import numpy as np
import plotly.graph_objects as go


hdb_carpark = pd.read_csv('hdb-carpark-lat-lon.csv')

type_of_carpark = list(hdb_carpark['car_park_type'].unique())
type_of_carpark.insert(0, "ALL")

type_options = st.multiselect(
    'Choose the type of carpark',
    type_of_carpark)

if type_options == ['ALL']:
    hdb_carpark_bytype = hdb_carpark
else:
    hdb_carpark_bytype = hdb_carpark[hdb_carpark['car_park_type'].isin(type_options)]

hdb_carpark_final = hdb_carpark_bytype.copy()

input_lat = 1.368112
input_lon = 103.804584
input_zoom = 10.5

postal_code = st.text_input('Key in postal code/address', value = '')

if postal_code != '':
    url = 'https://developers.onemap.sg/commonapi/search?searchVal=' + postal_code + '&returnGeom=Y&getAddrDetails=Y'
    response = requests.get(url)
    json_data = response.json()
    input_lat = float(json_data['results'][0]['LATITUDE'])
    input_lon = float(json_data['results'][0]['LONGITUDE'])
    input_zoom = 15

#st.map(hdb_carpark)
destination_df = pd.DataFrame({'lat': [input_lat], 'lon':[input_lon]})

#reference to these documentations
#https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart
#https://plotly.com/python/scattermapbox/

fig = go.Figure(go.Scattermapbox(
    lat = hdb_carpark_final['lat'],
    lon = hdb_carpark_final['lon'],
    mode = 'markers',
    marker = dict(
        size = 8,
        color='rgba(203, 29, 23, 0.8)',
        opacity = 0.5),
    text = hdb_carpark_final['address'],
    hovertemplate = '%{text}<extra></extra>'
))


if (input_lat != 1.368112) and (input_lon != 103.804584):
    fig.add_trace(go.Scattermapbox(
        lat = [input_lat],
        lon = [input_lon],
        mode = 'markers',
        marker = dict(
            symbol = 'circle',
            size = 10,
            color = 'rgba(30, 97, 238, 0.8)'),
        hovertemplate = 'Your Destination<extra></extra>'
        )
    )

fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    autosize = False,
    width = 700,
    height = 500,
    showlegend = False,
    hovermode = 'closest',
    mapbox_style="carto-positron",
    mapbox = dict(
        bearing = 0,
        center = dict(
            lat = input_lat,
            lon = input_lon),
        pitch = 0,
        zoom = input_zoom
    )
    )



st.plotly_chart(fig, use_container_width = True)