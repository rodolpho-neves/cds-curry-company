### ================================================ ###
### Construcao do dashboard Curry India Food Delivery ###
### ================================================ ###

### Importando as bibliotecas 
import pandas as pd
import numpy as np
import plotly.express as px
import folium # biblioteca para mapas
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

from utils import *


st.set_page_config(
    page_title="Visão Empresa",
    page_icon="🔨",
    layout="wide"
)

### Importando o DataFrame da Curry India Food Delivery
df_raw = pd.read_csv('./dataset/train.csv')
logo = Image.open('currylogo.png')

### Limpeza do banco de dados
# criando uma copia do dataframe
df = df_raw.copy()
# aplicando a funcao modular de limpeza
df = clean_df(df)

# =========================================
# Dashboard em Streamlit
# =========================================

st.header('Marketplace - Visão da Empresa')


# Sidebar do Dashboard
st.sidebar.image(logo,width=100)
st.sidebar.markdown('# Curry Company') 
st.sidebar.markdown('###### Fatest delivery in town!') 
st.sidebar.markdown("""---""") 

date_slider = st.sidebar.slider(
    'Data de interesse:',
    value = pd.datetime(2022,3,12),
    min_value = pd.datetime(2022, 2, 11),
    max_value = pd.datetime(2022, 4, 6),
    format = 'DD-MM-YYYY')

st.sidebar.markdown("""---""") 

traffic_options = st.sidebar.multiselect(
    'Quais condições de trânsito?',
    df['Road_traffic_density'].unique(),
    default = df['Road_traffic_density'].unique() )

st.sidebar.markdown("""---""") 

st.sidebar.markdown('###### Powered by Comunidade DS') 
st.sidebar.markdown("""---""") 

# Processandos os filtros
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas,:]

linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas,:]

# ===================================
# Layout principal
# ===================================


#st.dataframe( df )

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.markdown('### Orders by day')
        # Grafico de pedidos por dia
        df_aux = df[['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
        fig = px.bar(df_aux, x='Order_Date', y='ID')

        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('### Orders')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('#### by traffic density')
            fig = pie_ID_RoadTraffic(df)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('#### by traffic density and city')
            fig = scatter_ID_Road_City(df)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        st.markdown('### Order per week')
        # Pedidos por semana
        df_aux = df[['Week_of_year', 'ID']].groupby('Week_of_year').count().reset_index()
        fig = px.line(df_aux, x='Week_of_year', y='ID')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('### Order share by week')
        fig = line_ordershare_week(df)
        st.plotly_chart(fig, use_container_width=True)
    


with tab3:
    with st.container():
        map_order(df)