import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

class MapConfigWidget():
    def __init__(self, index, ids):
        self.index = index
        self.ids = ids
        self.data_type = st.selectbox("Data Type", ['Deployments', 'Latencies'], key=index)
        if self.data_type == 'Deployments':
            self.map_type = st.radio("Map Type",['HeatMap', 'DotMap'], key=index)
        else:
            self.map_type = 'ArcMap'
            self.id_selection = st.selectbox("Select a node ID", self.ids, key=index)
            self.min_value = st.slider("Min Threshold", 0, 300, 0, key=index)
            self.max_value = st.slider("Max Threshold", 0, 300, 300, key=index)
            self.color_value = st.slider("Color Threshold", 0, 300, 85, key=index)

def generate_arc_map(data, lat, lon, zoom, id, min_value=0, max_value=300, color_value=100):

    # pre filtering
    data = data[data['latencies'] > min_value]
    data = data[data['latencies'] < max_value]

    green_data = data[data['latencies'] < color_value]
    red_data = data[data['latencies'] > color_value]

    GREEN_RGB = [0, 255, 0, 40]
    RED_RGB = [240, 100, 0, 40]

    arc_layer_1 = pdk.Layer(
    "ArcLayer",
    data=green_data,
    get_width="(1/latencies)*350",
    get_source_position=["lon_s", "lat_s"],
    get_target_position=["lon", "lat"],
    get_tilt=15,
    get_source_color=GREEN_RGB,
    get_target_color=GREEN_RGB,
    pickable=False,
    auto_highlight=True,
    )
    arc_layer_2 = pdk.Layer(
    "ArcLayer",
    data=red_data,
    get_width="(1/latencies)*350",
    get_source_position=["lon_s", "lat_s"],
    get_target_position=["lon", "lat"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=RED_RGB,
    pickable=False,
    auto_highlight=True,
    )
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[arc_layer_1, arc_layer_2]
    ))

def generate_heat_map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))