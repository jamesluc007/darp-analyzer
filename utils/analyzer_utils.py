import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
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

def query_city_coordenates(address='Dubai'):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()

    if not response:
        return None

    df_cities = pd.DataFrame.from_dict(response[0])    
    df_cities = df_cities[['lat', 'lon']]
    df_cities = df_cities.astype(np.float16)
    df_cities = df_cities.drop(df_cities.index[range(1,len(df_cities.index))])

    return df_cities

def get_city_coordinates(address='Dubai'):

    df_cities = pd.read_csv('utils/city_coordinates.csv')  

    df_cities = df_cities.loc[df_cities['city'] == address]

    if df_cities is not None:
        return df_cities
    else:
        return query_city_coordenates(address=address)