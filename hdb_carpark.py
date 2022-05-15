from dataclasses import dataclass
import pandas as pd
import json
import requests
import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk
import numpy as np
import plotly.graph_objects as go
from itertools import compress


hdb_carpark = pd.read_csv('hdb-carpark-lat-lon.csv')

type_of_carpark = list(np.sort(hdb_carpark['car_park_type'].unique()))

short_term = list(np.sort(hdb_carpark['short_term_parking'].unique()))

with st.sidebar:

    #create checkbox for selection of type of carpark
    st.subheader('Choose Type of Carpark')

    col1, col2 = st.columns(2)

    with col1:
        surface = st.checkbox('SURFACE', True)
    with col2:
        ms = st.checkbox('MULTI-STOREY', True)

    col1, col2 = st.columns(2)

    with col1:
        surfacemulti = st.checkbox('SURFACE/MULTI-STOREY', True)
    with col2:
        basement = st.checkbox('BASEMENT', True)

    col1, col2 = st.columns(2)

    with col1:
        covered = st.checkbox('COVERED', True)
    with col2:
        mech = st.checkbox('MECHANISED', True)

    #line break between sections
    st.subheader('')

    #create checkbox for selection of short term parking
    st.subheader('Choose Short Term Parking')
    st.caption('Refers to parking in an HDB car park without a valid season parking.')

    col1, col2, = st.columns(2)

    with col1:
        show_wd = st.checkbox('Whole Day', True)
    with col2:
        show_no = st.checkbox('No', True)

    col1, col2 = st.columns(2)
    with col1:
        show_77 = st.checkbox('7am-7pm', True)  
    with col2:
        show_710 = st.checkbox('7am-10.30pm', True)

#filtering results based on selection

type_toggle = [basement, covered, mech, mech, ms, surface, surfacemulti]
type_options  = list(compress(type_of_carpark, type_toggle))

short_term_toggle = [show_710, show_77, show_no, show_wd]
short_term_options  = list(compress( short_term, short_term_toggle))

hdb_carpark_1 = hdb_carpark[hdb_carpark['car_park_type'].isin(type_options)]
hdb_carpark_2 = hdb_carpark_1[hdb_carpark_1['short_term_parking'].isin(short_term_options)]

hdb_carpark_final = hdb_carpark_2.copy()

input_lat = 1.368112
input_lon = 103.804584
input_zoom = 10.5

postal_code = st.text_input('Key in postal code/address', value = '')

if postal_code != '':
    url = 'https://developers.onemap.sg/commonapi/search?searchVal=' + postal_code + '&returnGeom=Y&getAddrDetails=Y'
    response = requests.get(url)
    json_data = response.json()
    if json_data['found'] > 0:
        input_lat = float(json_data['results'][0]['LATITUDE'])
        input_lon = float(json_data['results'][0]['LONGITUDE'])
        input_add = json_data['results'][0]['ADDRESS']
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
        text = [input_add],
        hovertemplate = 'YOUR DESTINATION:<br>' + '%{text}<extra></extra>'
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
else:
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
                lat = 1.368112,
                lon = 103.804584),
            pitch = 0,
            zoom = 10.5
        )
        )    



st.plotly_chart(fig, use_container_width = True)