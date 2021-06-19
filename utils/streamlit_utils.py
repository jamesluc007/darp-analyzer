import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

class MapConfigWidget():
    '''Class to define a webapp section for Maps Configurations.'''
    def __init__(self, index, ids):
        self.index = index
        self.ids = ids
        self.data_type = st.selectbox("Data Type", ['Deployments', 'Latencies'], key=index)
        st.caption("Deployments maps show the position of every running node on a world map.")
        st.caption("Latencies maps allow you to select one node and see all the conections to that node on a world map.")
        if self.data_type == 'Deployments':
            self.map_type = st.radio("Map Type",['HeatMap', 'DotMap'], key=index)
        else:
            self.map_type = 'ArcMap'
            self.id_selection = st.selectbox("Select a node ID", self.ids, key=index)
            st.caption("This map will show all the connections to node which id is: {}.".format(self.id_selection))
            self.min_value = int(st.slider("Min Threshold", 0, 300, 0, key=index))
            self.max_value = int(st.slider("Max Threshold", 0, 300, 300, key=index))
            st.caption("This map will show all the connections with latencies higher than {}ms and lower than {}ms".format(self.min_value, self.max_value))
            self.color_value = int(st.slider("Color Threshold", 0, 300, 85, key=index))
            st.caption("Latencies lower than {}ms will be shown in green. Latencies higher than {}ms will be shown in red.".format(self.color_value,self.color_value))

def generate_arc_map(data, lat, lon, zoom, id, min_value=0, max_value=300, color_value=100):
    '''Function to define PyDeck objects configurated for arc maps.'''
    # pre filtering
    try:
        # This fixes a bug caused when there is no latency data for an specific node
        data = data[data['latencies'] != 'N']
    except:
        pass    
    data['latencies'] = pd.to_numeric(data['latencies'])
    data = data[data['latencies'] > min_value]
    data = data[data['latencies'] < max_value]
    green_data = data[data['latencies'] < color_value]
    red_data = data[data['latencies'] > color_value]

    GREEN_RGB = [0, 255, 0, 40]
    RED_RGB = [240, 100, 0, 40]

    # map layer definitions:
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
    # map definition:
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
    '''Function to define PyDeck objects configurated for heat maps.'''
    # map definition:
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