import streamlit as st
import webbrowser
import pandas as pd
from datetime import datetime
import requests
import os

# para rodar no cmd, utilizar python -m streamlit run home.py
PHOTO_DIR = "assets/photos"

if "data" not in st.session_state:
    df_data = pd.read_csv("dataset/CLEAN_FIFA23_official_data.csv", index_col = 0)
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year] #Pega apenas jogadores cujo contrato é válido até o ano da data de hoje
    df_data = df_data[df_data["Value(£)"]>0] #Selecionando jogadores que possuem apenas o valor de mercado > 0
    df_data = df_data.sort_values(by="Overall", ascending = False) #Ordenando os valores por overall
    st.session_state["data"] = df_data


st.markdown('# FIFA23 OFFICIAL DATASET ⚽')
st.sidebar.markdown('Desenvolvido por [Victor Arruda](https://www.linkedin.com/in/victor-a-aa8a48140?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)')

btn = st.button('Acesse os dados do Kaggle') #Começa como false e após clique torna-se true

if btn:
    webbrowser.open_new_tab('https://www.kaggle.com/datasets/bryanb/fifa-player-stats-database')

st.markdown(
    """
    O conjunto de dados
de jogadores de futebol de 2017 a 2023 fornece informações
abrangentes sobre jogadores de futebol profissionais.
O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos
do jogador, características físicas, estatísticas de jogo, detalhes do contrato e
afiliações de clubes.

Com mais de 17.000 registros, este conjunto de dados oferece um recurso valioso para
analistas de futebol, pesquisadores e entusiastas interessados em explorar vários
aspectos do mundo do futebol, pois permite atributos de jogadores, métricas de
desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e
desenvolvimento do jogador ao longo do tempo.
"""
)

