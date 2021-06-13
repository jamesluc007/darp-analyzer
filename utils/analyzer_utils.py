import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import json
import yaml
import requests
import urllib.parse

def load_data(data_path, id=None):
    full_data_path = './data/{}'.format(data_path)
    data_files = [f for f in listdir(full_data_path) if isfile(join(full_data_path, f))]

    basePath = os.path.dirname(os.path.abspath(__file__))

    #list_of_data = []
    # This assumes that there is only one file in this location
    # Thus, previous data removal is necessary
    for i in data_files:
        if 'json' not in i:
            continue
        with open("{}/{}/{}".format(basePath,'../data/'+data_path,i)) as json_file:
            temp_dict = json.load(json_file)
        
        if id is not None:
            if temp_dict['groupId'] == id:
                return temp_dict
        else:
            return temp_dict
    
    return None

def update_data():
    os.system('sh ./data/load_data.sh')

def query_city_coordinates(address='Dubai'):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()

    if not response:
        #df_cities = pd.DataFrame()
        # Dangerous workaround for Å iauliai:
        df_cities = pd.DataFrame(columns=["lat", "lon", "city"], data=[[55.92,23.31, address]])
    else:
        df_cities = pd.DataFrame.from_dict(response[0])
        df_cities = df_cities[['lat', 'lon']]
        df_cities = df_cities.astype(np.float16)
        df_cities = df_cities.drop(df_cities.index[range(1,len(df_cities.index))])

    return df_cities

def get_city_coordinates(address='Dubai'):

    df_cities = pd.read_csv('utils/city_coordinates.csv')  

    df_cities.drop_duplicates(subset ="city",
                     keep = 'first', inplace = True)

    df_cities = df_cities.loc[df_cities['city'] == address]

    if not df_cities.empty:
        return df_cities
    else:
        temp = query_city_coordinates(address=address)
        temp['city'] = address
        return temp

def get_capital_city(country_prefix):

    with open('utils/country_prefixes.yml') as f:
        countries_dict = yaml.safe_load(f)
    
    df_capitals = pd.read_csv('utils/country_list.csv')

    df_capitals = df_capitals.loc[df_capitals['country'] == countries_dict[country_prefix]]

    return df_capitals['capital'].iloc[0]

