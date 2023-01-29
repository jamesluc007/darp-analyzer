import streamlit as st
import pandas as pd
import numpy as np

from utils.analyzer_utils import load_data, get_capital_city, get_city_coordinates, map_preprocessing
from utils.streamlit_utils import generate_arc_map, generate_heat_map, MapConfigWidget
from make import update_data

# WEB APP DEFINITION


class WebApp:

    """Main WebApp class. This class handles all the front-end stuff."""

    def __init__(self):
        # Attributes Initialization:
        self.groups_df = pd.DataFrame()
        self.latencies_df = pd.DataFrame()
        self.config_dict = {}
        self._update_data()

        # Sections Initialization:
        st.write("These are the current running DARP nodes:")
        st.write(self.groups_df)
        self.configuration()
        self.update_data_button()
        self.execute()

    def configuration(self):
        """Configuration Section. This handles all the user entries for later visualization generation."""

        st.header("Configure your Visuals:")

        self.config_dict["checkbox_raw"] = st.checkbox("Raw Data Visualization", False)
        st.caption("This generates a big table with all the latency readings.")

        self.config_dict["checkbox_map"] = st.checkbox("Map Visualization", False)
        st.caption("This enables Map Visualizations.")
        if self.config_dict["checkbox_map"]:
            self.config_dict["maps_number"] = st.slider("Number of Maps", 1, 4, 1)
            st.caption("Select the number of desired maps and expand the 'Maps Configuration' tab to configure them.")
            with st.beta_expander("Maps Configuration"):
                self.config_dict["maps"] = []
                for i in range(self.config_dict["maps_number"]):
                    st.write("Map number {}".format(i + 1))
                    self.config_dict["maps"].append(MapConfigWidget(i, self.groups_df["id"]))

        self.config_dict["machine_learning"] = st.checkbox("Trigger Machine Learning Prediction", False)
        st.caption("This enables the Machine Learning section (Not implemented yet).")

    def execute(self):
        """Buttons Section"""
        execute_button = st.button("Execute")
        if execute_button:
            self.raw_data_visualization()
            self.map_visualization()
            self.improvement_prediction()

    def update_data_button(self):
        """Button for updating DARP data from the server"""
        button = st.button("Update Data")
        if button:
            update_data()
            self._update_data()

    def _update_data(self):
        """Internal method for loading data from json files into pandas dataframes."""
        groups = load_data(data_path="groups")
        latencies = load_data(data_path="latencies")
        self.groups_df = pd.DataFrame.from_dict(groups["nodes"])
        self.latencies_df = pd.DataFrame.from_dict(latencies["matrix"])

        countries_list = [x for x in self.groups_df["country"]]
        new_cities_list = []
        for i, city in enumerate([x for x in self.groups_df["city"]]):
            if city is None:
                city = get_capital_city(countries_list[i])
            new_cities_list.append(city)
        self.groups_df["city"] = new_cities_list

    def raw_data_visualization(self):
        """Section to show the whole latencies table."""
        if self.config_dict["checkbox_raw"]:
            st.header("Raw Data Visualization")
            st.write(self.latencies_df)

    def map_visualization(self):
        """Section to show the user required maps."""
        if self.config_dict["checkbox_map"]:
            st.header("Map Visualization")
            for i, map_config in enumerate(self.config_dict["maps"]):
                st.write("Map Number {}:".format(i + 1))

                if map_config.map_type != "ArcMap":
                    local_group_df = map_preprocessing(self.groups_df.copy(), self.latencies_df.copy(), arc_map=False)
                else:
                    arc_df = map_preprocessing(self.groups_df.copy(), self.latencies_df.copy(), id_selection=map_config.id_selection, arc_map=True)

                if map_config.data_type == "Deployments":
                    if map_config.map_type == "HeatMap":
                        generate_heat_map(local_group_df, 0, 0, 1)
                    elif map_config.map_type == "DotMap":
                        st.map(local_group_df[["lat", "lon"]])

                elif map_config.data_type == "Latencies":
                    generate_arc_map(arc_df, 0, 0, 1, map_config.id_selection, map_config.min_value, map_config.max_value, map_config.color_value)

    def improvement_prediction(self):
        """Section to show Machine Learning Models outputs."""
        if self.config_dict["machine_learning"]:
            st.header("ML Modelling")
            st.write("here it goes my model")


# MAIN

st.title("DARP Analyzer Webapp")
st.write("This web app will create visualizations using DARP data.")

webapp = WebApp()
