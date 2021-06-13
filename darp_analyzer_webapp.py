import streamlit as st
import pandas as pd
import numpy as np

from utils.analyzer_utils import load_data, update_data, get_capital_city, query_city_coordinates, get_city_coordinates

# WEB APP DEFINITION

class WebApp():
    def __init__(self):
        self.groups_df = pd.DataFrame()
        self.latencies_df = pd.DataFrame()

        self._update_data()
        self.update_data_button()
        self.raw_data_visualization()
        self.map_visualization()
        self.improvement_prediction()
    
    def update_data_button(self):
        button = st.button('Update Data')
        if button:
            self._update_data()
    
    def _update_data(self):
        update_data()
        groups = load_data(data_path='groups')
        latencies = load_data(data_path='latencies')
        self.groups_df = pd.DataFrame.from_dict(groups['nodes'])
        self.latencies_df = pd.DataFrame.from_dict(latencies['matrix'])

    def raw_data_visualization(self):
        st.header("Raw Data Visualization")
        checkbox_raw = st.checkbox("Visualize Raw Data")
        if checkbox_raw:
            st.write(self.groups_df)
            st.write(self.latencies_df)
    
    def map_visualization(self):
        st.header("Map Visualization")
        checkbox_map = st.checkbox("Visualize Map")
        if checkbox_map:
            df_map = pd.DataFrame()
            countries_list = [x for x in self.groups_df['country']]
            for i, city in enumerate([x for x in self.groups_df['city']]):

                if city is None:
                    city = get_capital_city(countries_list[i])

                temp_df = get_city_coordinates(address=str(city))
                df_map = df_map.append(temp_df)

            #st.write(df_map)        
            self.groups_df = pd.merge(self.groups_df, df_map, on='city')        
            st.write(self.groups_df)
            st.map(self.groups_df[['lat', 'lon']])
            
    def improvement_prediction(self):
        st.header("ML Modelling")


# MAIN

st.title("DARP Analyzer Webapp")
st.write("This web app will help you to visualize and analyze your DARP data.")
webapp = WebApp()
    