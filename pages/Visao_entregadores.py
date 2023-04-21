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

# 📚⚙️⚛️💅🌏🛢🍪🤐🦀🧪🐞⚠️🚨🚀🔨💡🗑👷‍♂️🔒🏞🎞🔈📂📦

st.set_page_config(
    page_title="Visão Entregadores",
    page_icon="🚀",
    layout="wide"
)

### Importando o DataFrame da Curry India Food Delivery
df_raw = pd.read_csv('./dataset/train.csv')
logo = Image.open('currylogo.png')

### Limpeza do banco de dados
# criando uma copia do dataframe
df = df_raw.copy()
df = clean_df(df)

# =========================================
# Dashboard em Streamlit
# =========================================

st.header('Marketplace - Visão dos Entregadores')


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

weather_options = st.sidebar.multiselect(
    'Quais condições climáticas?',
    df['Weatherconditions'].unique(),
    default = df['Weatherconditions'].unique() )

st.sidebar.markdown("""---""") 

st.sidebar.markdown('###### Powered by Comunidade DS') 
st.sidebar.markdown("""---""") 

# Processandos os filtros
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas,:]

linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas,:]

linhas_selecionadas = df['Weatherconditions'].isin(weather_options)
df = df.loc[linhas_selecionadas,:]

# ===================================
# Layout principal
# ===================================


#st.dataframe( df )

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
    with st.container():
        st.markdown('### Overall metrics')
        col1, col2, col3, col4 = st.columns(4, gap='Large')
        with col1:
            menor_idade = df['Delivery_person_Age'].min()
            col1.metric('Menor idade', menor_idade)

        with col2:
            maior_idade = df['Delivery_person_Age'].max()
            col2.metric('Maior idade', maior_idade)
        
        with col3:
            pior_condicao_veiculo = df['Vehicle_condition'].min()
            col3.metric('Pior veículo', pior_condicao_veiculo)
        
        with col4:
            melhor_condicao_veiculo = df['Vehicle_condition'].max()
            col4.metric('Melhor veículo', melhor_condicao_veiculo)

        st.markdown("""---""")

    with st.container():
        st.markdown('## Ratings')

        col1, col2= st.columns(2, gap='Large')
        with col1:
            with st.container():

                df_aux = df[['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').agg(['mean', 'std'])
                df_aux.columns = ['Ratings_mean', 'Ratings_std']
                df_aux.reset_index()

                st.markdown('##### Rating by delivery person')
                st.dataframe( df_aux )

        with col2:
            with st.container():
                
                df_aux = df[['Road_traffic_density','Delivery_person_Ratings']].groupby('Road_traffic_density').agg(['mean', 'std'])
                df_aux.columns = ['Ratings_mean', 'Ratings_std']
                df_aux.reset_index()

                st.markdown('##### Ratings by traffic')
                st.dataframe( df_aux )

            
            with st.container():
                df_aux = df[['Weatherconditions','Delivery_person_Ratings']].groupby('Weatherconditions').agg(['mean', 'std'])
                df_aux.columns = ['Ratings_mean', 'Ratings_std']
                df_aux.reset_index()

                st.markdown('##### Rating by weather condition')
                st.dataframe( df_aux )
            

        st.markdown("""---""")

    with st.container():
        st.markdown('### Delivery speed')

        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                st.markdown('##### Top Fastest Delivery by City')
                df_aux = df[['Delivery_person_ID', 'Time_taken(min)', 'City']].groupby(['City','Delivery_person_ID']).min().reset_index().sort_values(by='Time_taken(min)',ascending=True)
                for i in range(len(df_aux['City'].unique())):
                    if i == 0: 
                        df_aux_faster = df_aux.loc[df_aux['City'] == df_aux['City'].unique()[i],: ][:10]
                    else:
                        df_aux_faster = pd.concat([df_aux_faster, df_aux.loc[df_aux['City'] == df_aux['City'].unique()[i],: ][:10]], ignore_index=True)
                st.dataframe(df_aux_faster)
                
        
        with col2:
            with st.container():
                st.markdown('##### Top Slowest Delivery by City')
                df_aux = df[['Delivery_person_ID', 'Time_taken(min)', 'City']].groupby(['City','Delivery_person_ID']).max().reset_index().sort_values(by='Time_taken(min)',ascending=False)
                for i in range(len(df_aux['City'].unique())):
                    if i == 0: 
                        df_aux_slower = df_aux.loc[df_aux['City'] == df_aux['City'].unique()[i],: ][:10]
                    else:
                        df_aux_slower = pd.concat([df_aux_slower, df_aux.loc[df_aux['City'] == df_aux['City'].unique()[i],: ][:10]], ignore_index=True)
                st.dataframe(df_aux_slower)
        
        st.markdown("""---""")

with tab2:
    pass
    


with tab3:
    pass