import streamlit as st
import pandas as pd
import numpy as np

from utils.analyzer_utils import load_data, get_capital_city, get_city_coordinates, map_preprocessing
from utils.streamlit_utils import generate_arc_map, generate_heat_map, MapConfigWidget
from make import update_data

# WEB APP DEFINITION

class WebApp():
    def __init__(self):
        self.groups_df = pd.DataFrame()
        self.latencies_df = pd.DataFrame()

        self.config_dict = {}
        self._update_data()
        st.write("These are the current running DARP nodes:")
        st.write(self.groups_df)
        self.configuration()
        self.execute()
        
        self.update_data_button()
    
    def configuration(self):
        st.header("Configure your Visuals:")
        self.config_dict['checkbox_raw'] = st.checkbox("Raw Data Visualization", False) #st.checkbox("Visualize Raw Data")
        self.config_dict['checkbox_map'] = st.checkbox("Map Visualization", False)
        if self.config_dict['checkbox_map']:
            self.config_dict['maps_number'] = st.slider("Number of Maps", 1, 4, 1)
            with st.beta_expander("Maps Configuration"):
                self.config_dict['maps']=[]
                for i in range(self.config_dict['maps_number']):
                    st.write("Map number {}".format(i+1))
                    self.config_dict['maps'].append(MapConfigWidget(i, self.groups_df['id']))

        self.config_dict['machine_learning'] = st.checkbox("Trigger Machine Learning Prediction", False)
    
    def execute(self):
        execute_button = st.button('Execute')
        if execute_button:
            self.raw_data_visualization()
            self.map_visualization()
            self.improvement_prediction()
    
    def update_data_button(self):
        button = st.button('Update Data')
        if button:
            update_data()
            self._update_data()
    
    def _update_data(self):
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
        if self.config_dict['checkbox_raw']:
            st.header("Raw Data Visualization")
            st.write(self.latencies_df)
    
    def map_visualization(self):
        if self.config_dict['checkbox_map']:
            st.header("Map Visualization")
            for i, map_config in enumerate(self.config_dict['maps']):     
                st.write("Map Number {}:".format(i+1))      

                if map_config.map_type!='ArcMap':
                    local_group_df, arc_df = map_preprocessing(self.groups_df,self.latencies_df, arc_map=False)
                else:
                    local_group_df, arc_df = map_preprocessing(self.groups_df,self.latencies_df, id_selection=map_config.id_selection,arc_map=True)
                
                if map_config.data_type == 'Deployments':
                    if map_config.map_type == 'HeatMap':
                        generate_heat_map(local_group_df,0,0,1)
                    elif map_config.map_type == 'DotMap':
                        st.map(local_group_df[['lat', 'lon']])

                elif map_config.data_type == 'Latencies':
                    generate_arc_map(arc_df,0,0,1,map_config.id_selection, map_config.min_value, map_config.max_value, map_config.color_value)         
    
    def improvement_prediction(self):
        if self.config_dict['machine_learning']:
            st.header("ML Modelling")
            st.write("here it goes my model")

# MAIN

st.title("DARP Analyzer Webapp")
st.write("This web app will help you to visualize and analyze your DARP data.")

webapp = WebApp()    