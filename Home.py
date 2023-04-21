import streamlit as st
from PIL import Image
from utils import *


# 📚⚙️⚛️💅🌏🛢🍪🤐🦀🧪🐞⚠️🚨🚀🔨💡🗑👷‍♂️🔒🏞🎞🔈📂📦

st.set_page_config(
    page_title="Home",
    page_icon="🚨",
    layout="centered"
)


# Sidebar do Dashboard 
image_path = "currylogo.png"
logo = Image.open(image_path)

st.sidebar.image(logo,width=120)
st.sidebar.markdown('# Curry Company') 
st.sidebar.markdown('###### Fatest delivery in town!') 
st.sidebar.markdown("""---""") 

st.markdown("# Curry Company Growth Dashboard")
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar este Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurantes: 
        - Indicadores semanais de crescimento dos restaurantes
    
    ### Ask for help:
    - Time de Data Science no Discord
        - @rodolpho.neves
    """
    )