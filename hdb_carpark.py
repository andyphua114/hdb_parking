from dataclasses import dataclass
import pandas as pd
import json
import requests
import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk
import numpy as np


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

postal_code = st.text_input('Key in postal code', value = '')

input_lat = 1.365797
input_lon = 103.813517
input_zoom = 11
if postal_code == '733894':
    input_lat = 1.43563830011225
    input_lon = 103.789459334951
    input_zoom = 16

#st.map(hdb_carpark)
destination_df = pd.DataFrame({'lat': [input_lat], 'lon':[input_lon]})

#reference to these documentations
#https://deck.gl/docs/api-reference/layers
#https://deckgl.readthedocs.io/en/latest/gallery/scatterplot_layer.html
#https://deckgl.readthedocs.io/en/latest/tooltip.html
#https://deckgl.readthedocs.io/en/latest/gallery/icon_layer.html
st.pydeck_chart(pdk.Deck(
    map_style = 'mapbox://styles/mapbox/streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=input_lat,
        longitude=input_lon,
        zoom=input_zoom,
        pitch=0,
    ),
    layers = [
        pdk.Layer(
            'ScatterplotLayer',
            data = hdb_carpark_final,
            pickable = True,
            get_position = '[lon, lat]',
            get_color = '[200, 30, 0, 160]',
            get_radius = 15
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data = destination_df,
            pickable = True,
            get_position = '[lon, lat]',
            get_color = '[0, 44, 199, 160]',
            get_radius = 15   
        )           
    ],
    tooltip = {
        'text': "{car_park_type}\n{address}",

    }    
))