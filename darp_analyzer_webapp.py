import streamlit as st
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import subprocess
import json
import requests
import urllib.parse

def load_data(data_path, id=None):
    full_data_path = './data/{}'.format(data_path)
    data_files = [f for f in listdir(full_data_path) if isfile(join(full_data_path, f))]

    basePath = os.path.dirname(os.path.abspath(__file__))

    list_of_data = []
    # This assumes that there is only one file in this location
    # Thus, previous data removal is necessary
    for i in data_files:
        if 'json' not in i:
            continue
        with open("{}/{}/{}".format(basePath,'data/'+data_path,i)) as json_file:
            temp_dict = json.load(json_file)
        
        if id is not None:
            if temp_dict['groupId'] == id:
                return temp_dict
        else:
            return temp_dict
    
    return None

def update_data():
    os.system('sh ./data/load_data.sh')

def get_coordenates(address='Dubai'):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()

    if not response:
        return None

    df = pd.DataFrame.from_dict(response[0])    
    df = df[['lat', 'lon']]
    df = df.astype(np.float16)
    df = df.drop(df.index[range(1,len(df.index))])

    return df

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
        
        df = pd.DataFrame()
        for i in [x for x in self.groups_df['city']][:1]:
            if i is None:
                continue
            temp_df = get_coordenates(address=i)
            if temp_df is not None:
                df = df.append(temp_df)

        st.write(df)
        st.map(df[['lat', 'lon']])
            
    def improvement_prediction(self):
        st.header("ML Modelling")


# MAIN

st.title("DARP Analyzer Webapp")
st.write("This web app will help you to visualize and analyze your DARP data.")
webapp = WebApp()

    