import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import os
import json
import yaml
import requests
import urllib.parse
import streamlit as st
from typing import Tuple


def load_data(data_path: str, id: str = None):
    """
    This method loads data from darp json files and converts it into python dictionaries.
    data_path: String with relative folder location of JSon files.
    It tipically is "latencies" or "groups"
    id: str with Required ID. For hackathon purposes, it can be ignored.
    """
    full_data_path = "./data/{}".format(data_path)
    data_files = [f for f in listdir(full_data_path) if isfile(join(full_data_path, f))]
    if not data_files:
        raise AssertionError("load_data method could not find any JSon file to load data from.")

    basePath = os.path.dirname(os.path.abspath(__file__))

    for i in data_files:
        if "json" not in i:
            continue
        with open("{}/{}/{}".format(basePath, "../data/" + data_path, i)) as json_file:
            temp_dict = json.load(json_file)

        if id is not None:
            if temp_dict["groupId"] == id:
                return temp_dict
        else:
            return temp_dict

    raise AssertionError("load_data method could not find any JSon file with the data of required id.")


def query_city_coordinates(address: str = "Dubai") -> pd.DataFrame:
    """
    This method gets the requested city coordinates using an open source server.
    It uses a REST API of a popular website. It takes a considerable amount of time.
    Should only be used if the coordinates are not in a typical cache CSV.
    """
    url = "https://nominatim.openstreetmap.org/search/" + urllib.parse.quote(address) + "?format=json"
    response = requests.get(url).json()

    if not response:
        # FIXME:
        # Very dangerous workaround for Å iauliai city (Python has trouble processing the "Å" character):
        # In practice, that is the only city that gave me trouble.
        # So for hackathon purposes, if the REST API can't return a value, assume it's that city.
        df_cities = pd.DataFrame(columns=["lat", "lon", "city"], data=[[55.92, 23.31, address]])
    else:
        # Take only "lat" and "lon" columns and make sure they are floats.
        # Keep only the first row
        df_cities = pd.DataFrame.from_dict(response[0])
        df_cities = df_cities[["lat", "lon"]]
        df_cities = df_cities.astype(np.float16)
        df_cities = df_cities.drop(df_cities.index[range(1, len(df_cities.index))])

    df_cities["city"] = address

    return df_cities


def get_city_coordinates(address: str = "Dubai") -> pd.DataFrame:
    """
    This method gets the requested city coordinates using a csv file with usual cities data.
    It is very fast. If it does not find the city in the CSV, it calls method query_city_coordinates.
    """
    df_cities = pd.read_csv("utils/city_coordinates.csv")
    df_cities.drop_duplicates(subset="city", keep="first", inplace=True)

    df_cities = df_cities.loc[df_cities["city"] == address]

    if not df_cities.empty:
        return df_cities
    else:
        return query_city_coordinates(address=address)


def get_capital_city(country_prefix: str = "AE") -> str:
    """
    This method returns the capital city of a given country.
    This is usefull for DARP nodes which do not have declared cities.
    """
    with open("utils/country_prefixes.yml") as f:
        countries_dict = yaml.safe_load(f)

    df_capitals = pd.read_csv("utils/country_list.csv")

    df_capitals = df_capitals.loc[df_capitals["country"] == countries_dict[country_prefix]]

    # FIXME: Change previous line by this one (easier to read):
    # df_capitals = df_capitals[df_capitals.country == countries_dict[country_prefix]]

    return df_capitals["capital"].iloc[0]


def map_preprocessing(data: pd.DataFrame, latencies_input: pd.DataFrame, id_selection: int = 0, arc_map: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    This method perfoms the preprocessinng method for maps generation.
    data: Data Frame with the Group information (Country, City, etc)
    latencies_input: Data Frame with Latencies Matrix information
    It returns a dataframe. If user wants an "arc_map" it returns arc_df. Otherwise it returns local_group_df.
    local_group_df is a processed version of data input.
    """
    df_map = pd.DataFrame()
    local_group_df = data.copy()

    for city in [x for x in local_group_df["city"]]:
        df_map = df_map.append(get_city_coordinates(address=str(city)))

    # Add city coordinates to local_group_df
    local_group_df = pd.merge(local_group_df, df_map, on="city")
    # Drop duplicates and reset_index
    local_group_df.drop_duplicates(subset="id", keep="first", inplace=True)
    local_group_df = local_group_df.reset_index(drop=True)

    if not arc_map:
        return local_group_df
    else:
        # Add a column with all the latencies in reference with id_selected node
        index = local_group_df.loc[local_group_df["id"] == id_selection].index[0]
        latencies = pd.Series.to_frame(latencies_input[index])
        latencies = latencies.rename(columns={index: "latencies"})
        local_group_df = pd.concat([local_group_df, latencies], axis=1, join="inner")

        # Add columns with the latitude and longitude of the id_selected node
        # Arrange data as it's expected by the map generation library
        arc_df = local_group_df[["id", "lat", "lon", "latencies"]].drop([index])

        temp_lat = local_group_df.iloc[index]["lat"]
        temp_lon = local_group_df.iloc[index]["lon"]
        n_rows = arc_df.shape[0]
        lat_s = pd.DataFrame.from_dict({"lat_s": [temp_lat for i in range(1, n_rows + 1)]})
        lon_s = pd.DataFrame.from_dict({"lon_s": [temp_lon for i in range(1, n_rows + 1)]})

        arc_df = pd.concat([arc_df, lat_s], axis=1, join="inner")
        arc_df = pd.concat([arc_df, lon_s], axis=1, join="inner")
        arc_df = arc_df.reset_index(drop=True)

        return arc_df
