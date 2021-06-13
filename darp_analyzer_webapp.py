import streamlit as st
import pandas as pd
import numpy as np

from utils.analyzer_utils import load_data, update_data, get_capital_city, query_city_coordinates, get_city_coordinates

# WEB APP DEFINITION

class WebApp():
    def __init__(self):
        self.groups_df = pd.DataFrame()
        self.latencies_df = pd.DataFrame()

        self.configuration_dict = {}
        self._update_data()
        self.configuration()
        self.execute()
        
        self.update_data_button()
    
    def configuration(self):
        st.header("Select your configuration:")
        self.configuration_dict['checkbox_raw'] = st.checkbox("Visualize Raw Data")
        self.configuration_dict['checkbox_map'] = st.checkbox("Visualize Map")
        self.configuration_dict['machine_learning'] = st.checkbox("Trigger Machine Learning Prediction")
    
    def execute(self):
        execute_button = st.button('Execute')
        if execute_button:
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

        countries_list = [x for x in self.groups_df['country']]
        new_cities_list = []
        for i, city in enumerate([x for x in self.groups_df['city']]):
            if city is None:
                city = get_capital_city(countries_list[i])
            new_cities_list.append(city)
        self.groups_df['city'] = new_cities_list



    def raw_data_visualization(self):
        if self.configuration_dict['checkbox_raw']:
            st.header("Raw Data Visualization")
            st.write(self.groups_df)
            st.write(self.latencies_df)
    
    def map_visualization(self):
        
        if self.configuration_dict['checkbox_map']:
            st.header("Map Visualization")
            df_map = pd.DataFrame()
            countries_list = [x for x in self.groups_df['country']]
            for i, city in enumerate([x for x in self.groups_df['city']]):

                if city is None:
                    city = get_capital_city(countries_list[i])

                temp_df = get_city_coordinates(address=str(city))
                df_map = df_map.append(temp_df)

            #st.write(df_map)        
            self.groups_df = pd.merge(self.groups_df, df_map, on='city')     
            self.groups_df.drop_duplicates(subset ="id",
                    keep = 'first', inplace = True)  
            self.groups_df = self.groups_df.reset_index(drop=True) 
            st.write(self.groups_df)
            st.map(self.groups_df[['lat', 'lon']])
            
    def improvement_prediction(self):
        if self.configuration_dict['machine_learning']:
            st.header("ML Modelling")


# MAIN

st.title("DARP Analyzer Webapp")
st.write("This web app will help you to visualize and analyze your DARP data.")
webapp = WebApp()
    