import streamlit as st
import os
from urllib.parse import urlparse

st.set_page_config(
    page_title = 'Players',
    page_icon = '🏃‍♀️‍➡️',
    layout = 'wide'
)
df_data = st.session_state["data"]

PHOTO_DIR = "assets/photos"

# 1) Padroniza a coluna Photo (se ainda estiver como URL)
#    Só faz se parecer URL; senão, deixa como está (já nome de arquivo).
if df_data["Photo"].astype(str).str.startswith("http").any():
    df_data["Photo"] = (
        df_data["Photo"]
        .astype(str)
        .apply(lambda u: urlparse(u).path.strip("/").replace("/", "_"))
    )

# 2) Remove jogadores sem imagem local
def imagem_existe(photo_name):
    if not photo_name or photo_name == "nan":
        return False
    photo_path = os.path.join(PHOTO_DIR, str(photo_name).strip())
    return os.path.exists(photo_path)

df_data["has_image"] = df_data["Photo"].apply(imagem_existe)

# Mantém apenas jogadores com imagem
df_data = df_data[df_data["has_image"]].copy()

# 3) Filtros
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# 4) Linha do jogador selecionado
player_stats = df_players[df_players["Name"] == player].iloc[0]

# 5) Monta caminho local e printa
photo_name = str(player_stats["Photo"]).strip()
photo_path = os.path.join(PHOTO_DIR, photo_name)

if os.path.exists(photo_path):
    st.image(photo_path, width=60)
else:
    st.warning(f"Foto não encontrada: {photo_path}")

st.title(player_stats["Name"])

#Com o f na frente, é possivel colocar variáveis dentro do texto
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

#Criando as colunas para idade, altura e peso
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)']/100}") #A altura está em cm, convertendo para m
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.2f}") #Convertendo de libras para kg e colocando 2 casas decimais
st.divider()
st.subheader(f"**Overall: {player_stats['Overall']}**")
st.progress(int(player_stats['Overall']))

#Criando as colunas para idade, altura e peso
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor de mercado", value=f"€ {player_stats['Value(£)']:,}")
col2.metric(label="Remuneração semanal", value=f"€ {player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de rescisão", value=f"€ {player_stats['Release Clause(£)']:,}")