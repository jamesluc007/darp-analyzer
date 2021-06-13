import streamlit as st
import pandas as pd
import numpy as np

from utils.analyzer_utils import load_data, update_data, query_city_coordenates, get_city_coordinates

# WEB APP DEFINITION

class WebApp():
    def __init__(self):
        self.groups_df = pd.DataFrame()
        self.latencies_df = pd.DataFrame()

        self.update_data_button()
        self.raw_data_visualization()
        self.map_visualization()
        self.improvement_prediction()
    
    def update_data_button(self):
        button = st.button('Update Data')
        if button:
            update_data()
            groups = load_data(data_path='groups')
            latencies = load_data(data_path='latencies')
            self.groups_df = pd.DataFrame.from_dict(groups['nodes'])
            self.latencies_df = pd.DataFrame.from_dict(latencies['matrix'])

    def raw_data_visualization(self):
        st.header("Raw Data Visualization")
        checkbox = st.checkbox("Visualize")
        if checkbox:
            st.write(self.groups_df)
            st.write(self.latencies_df)
    
    def map_visualization(self):
        st.header("Map Visualization")
        
        df_map = pd.DataFrame()
        for i in [x for x in self.groups_df['city']]:
            if i is None:
                continue
            temp_df = get_city_coordinates(address=i)
            if temp_df is not None:
                df_map = df_map.append(temp_df)

        st.write(df_map)
        st.map(df_map[['lat', 'lon']])
            
    def improvement_prediction(self):
        st.header("ML Modelling")


# MAIN

st.title("DARP Analyzer Webapp")
st.write("This web app will help you to visualize and analyze your DARP data.")
webapp = WebApp()

    