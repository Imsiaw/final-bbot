import pandas as pd
import streamlit as st
import os
from mitosheet.streamlit.v1 import spreadsheet
import streamlit_extras as ste
import uuid
from datetime import datetime

# ------------------------------------------------------------

os.system("clear")

bbot_path = "bbot"

diff_path = "diff"

if "active_directory" not in st.session_state:
    st.session_state["active_directory"] = None

active_directory = None

st.set_page_config(
    page_title="BBot CSV Explorer",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded",
)

sidebar = st.sidebar


def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


create_dir_if_not_exist(bbot_path)
create_dir_if_not_exist(diff_path)


def button_callback(path):
    st.session_state["active_directory"] = path


# ------------------------------------------------------------


if st.session_state["active_directory"] != None:
    base_path = st.session_state["active_directory"]
    st.header(base_path)
    csv_path = base_path
    df = pd.read_csv(csv_path, index_col=None)
    new_dfs, code = spreadsheet(df, df_names=[os.path.basename(base_path)])
    st.write(new_dfs, unsafe_allow_html=True)
    st.code(code)


# ------------------------------------------------------------


bbot_directories = [
    d for d in os.listdir(bbot_path) if os.path.isdir(os.path.join(bbot_path, d))
]

if len(bbot_directories) != 0:
    sidebar.header("Project's")

bbot_files = []

for dir in bbot_directories:
    path = f"{bbot_path}/{dir}"
    sub_dirs = [
        d
        for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
        and "asset-inventory.csv" in os.listdir(f"{path}/{d}")
    ]
    bbot_files.append({"label": dir, "children": sub_dirs})


for dir in bbot_files:
    with sidebar.expander(dir["label"]):
        date_list = dir["children"]
        date_list = sorted(
            date_list,
            key=lambda x: datetime.strptime(x, "%Y_%m_%d_%H%M%S"),
            reverse=True,
        )
        for file in date_list[:3]:
            path = f"{bbot_path}/{dir['label']}/{file}/asset-inventory.csv"
            st.button(
                file,
                key=uuid.uuid4(),
                use_container_width=True,
                on_click=button_callback,
                args=(path,),
            )

# ------------------------------------------------------------
sidebar.divider()

diff_directories = [
    d for d in os.listdir(diff_path) if os.path.isdir(os.path.join(diff_path, d))
]


if len(diff_directories) != 0:
    sidebar.header("Diff's")

print(diff_directories)

diff_files = []

for dir in diff_directories:
    path = f"{diff_path}/{dir}"
    sub_dirs = [d for d in os.listdir(path) if d.endswith(".csv")]
    diff_files.append({"label": dir, "children": sub_dirs})

print(diff_files)


with sidebar.expander("Diff"):
    for dir in diff_files:
        with sidebar.expander(dir["label"]):
            for file in dir["children"]:
                print(file)
                path = f"{diff_path}/{dir['label']}/{file}"
                st.button(
                    file,
                    key=uuid.uuid4(),
                    use_container_width=True,
                    on_click=button_callback,
                    args=(path,),
                )
