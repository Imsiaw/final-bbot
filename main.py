import pandas as pd
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
import os
from mitosheet.streamlit.v1 import spreadsheet

# Get the current working directory
bbot_path = "bbot"

# Get a list of all the subdirectories in the current working directory
subdirs = [
    d
    for d in os.listdir(bbot_path)
    if os.path.isdir(os.path.join(bbot_path, d))
    and "asset-inventory.csv" in os.listdir(os.path.join(bbot_path, d))
]
st.set_page_config(
    page_title="BBot CSV Explorer",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded",
)

# Create a sidebar
sidebar = st.sidebar

# Add a selectbox to the sidebar to allow the user to select a subdirectory
subdir_selectbox = sidebar.selectbox("Select a Subdirectory", subdirs)

# Get the path to the selected subdirectory
subdir_path = os.path.join(bbot_path, subdir_selectbox)


# Get the path to the input.csv file in the selected subdirectory
input_csv_path = os.path.join(subdir_path, "asset-inventory.csv")


dfs = []

for dir in subdirs:
    path = os.path.join(bbot_path, dir)
    csv_path = os.path.join(path, "asset-inventory.csv")
    df = pd.read_csv(csv_path)
    dfs.append(df)

# Load the input.csv file into a pandas DataFrame
df = pd.read_csv(input_csv_path)

data_dict = df.to_dict()


df.index += 1

df.fillna("None", inplace=True)

# Add a header to the filter section
st.header(f"Data Filter in {subdir_selectbox}")

spreadsheet(*dfs)


# Define a function to update the URL with the selected subdirectory
def update_url():
    url = st.query_params
    url["subdir"] = subdir_selectbox


# Call the update_url function after selecting a subdirectory
update_url()
