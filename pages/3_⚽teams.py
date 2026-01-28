import streamlit as st
import os
from urllib.parse import urlparse
import requests
import base64


st.set_page_config(
    page_title = 'Players',
    page_icon = '🏃‍♀️‍➡️',
    layout = 'wide'
)

df_data = st.session_state["data"]

# 1) Filtros
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)
df_filtered_club = df_data[(df_data["Club"] == club)].set_index("Name") #Filtrando o data frame pelo clube selecionado e indexando pelo nome
#Ao invés de 1, 2, 3

def load_image_64(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers).content
    return "data:image/png;base64," + base64.b64encode(data).decode()

def preprocess_row(url):
    if isinstance(url, str) and url.startswith("http"):
        return load_image_64(url)
    return url

df_filtered_club["Photo"] = df_filtered_club["Photo"].apply(preprocess_row)
df_filtered_club["Flag"] = df_filtered_club["Flag"].apply(preprocess_row)
df_filtered_club["Club Logo"] = df_filtered_club["Club Logo"].apply(preprocess_row)

st.image(df_filtered_club.iloc[0]["Club Logo"], width=80)
st.markdown(f"## {club}")
columns = ["Age", "Photo", "Flag", "Overall", "Value(£)", "Wage(£)", "Joined", "Height(cm.)", "Weight(lbs.)", "Contract Valid Until", "Release Clause(£)"]

st.dataframe(df_filtered_club[columns],
            column_config={
                "Overall": st.column_config.ProgressColumn (
                    "Overall", format= "%d", min_value=0, max_value=100),
                "Wage(£)": st.column_config.ProgressColumn (
                    "Weekly Wage", format= "£%f", min_value=0, max_value=df_filtered_club["Wage(£)"].max()), #O valor que recebe mais será o limite da barra de remuneração
                "Photo": st.column_config.ImageColumn("Photo"),
                "Flag": st.column_config.ImageColumn("Flag")
            })#Data frame permite que você faça customização

