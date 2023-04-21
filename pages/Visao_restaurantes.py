### ================================================ ###
### Construcao do dashboard Curry India Food Delivery ###
### ================================================ ###

### Importando as bibliotecas 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium # biblioteca para mapas
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from utils import *

# 📚⚙️⚛️💅🌏🛢🍪🤐🦀🧪🐞⚠️🚨🚀🔨💡🗑👷‍♂️🔒🏞🎞🔈📂📦

st.set_page_config(
    page_title="Visão Restaurantes",
    page_icon="🦀",
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

st.header('Marketplace - Visão dos Restaurantes')


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
        col1, col2, col3 = st.columns(3, gap='Large')
        with col1:
            entregadores = df['Delivery_person_ID'].nunique()
            col1.metric('Entregadores', entregadores)

        with col2:
            df['Delivery_distance'] = ( df.loc[:,['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']]
                                            .apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                       (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1 ))

            distancia_media = np.round(df['Delivery_distance'].mean(), 2)
            col2.metric('Distância média (km)', distancia_media)
        
        with col3:
            df_aux = df[['City', 'Time_taken(min)']].groupby('City').agg(['mean', 'std'])
            df_aux.columns=['Time_mean', 'Time_std']
            df_aux = df_aux.reset_index()
            
            tempo_medio = np.round(df_aux['Time_mean'].mean(),2)
            col3.metric('Tempo médio (min)', tempo_medio)
        
        col4, col5, col6 = st.columns(3, gap='Large')
        
        with col6:
            std_tempo_medio = np.round(df_aux['Time_std'].mean(),2)
            col6.metric('STD tempo (min)', std_tempo_medio)

        with col4:
            tempo_medio_festival = np.round(df.loc[df['Festival'] == 'Yes',['Time_taken(min)']].mean().values[0],2)
            col4.metric('Tempo médio no Festival (min)', tempo_medio_festival)
        
        with col5:
            std_tempo_medio_festival = np.round(df.loc[df['Festival'] == 'Yes',['Time_taken(min)']].std().values[0],2)
            col5.metric('STD tempo no Festival (min)', std_tempo_medio_festival)

        st.markdown("""---""")

    with st.container():
        st.markdown('### Delivery time')

        col1, col2= st.columns(2, gap='Large')
        with col1:
            with st.container():
                st.markdown('#### Mean time by City')
                avg_distance = df[['City', 'Delivery_distance']].groupby('City').mean().reset_index()
                fig = go.Figure( data=[go.Pie(labels=avg_distance['City'], values=avg_distance['Delivery_distance'], pull=[0, 0.1, 0])])
                st.plotly_chart(fig, use_container_width=True)
            

        with col2:
            with st.container():
                st.markdown('#### Mean time and STD time by City')
                df_aux = df[['City', 'Time_taken(min)']].groupby('City').agg(['mean', 'std'])
                df_aux.columns=['Time_mean', 'Time_std']
                df_aux = df_aux.reset_index()

                fig = go.Figure(go.Bar(name='Control', x=df_aux['City'], y=df_aux['Time_mean'], error_y=dict(type='data', array=df_aux['Time_std'])))
                fig.update_layout(barmode = 'group')
                st.plotly_chart(fig, use_container_width=True)
            

        st.markdown("""---""")

    with st.container():
        st.markdown('### Delivery speed')

        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                st.markdown('##### Mean time and STD time by City and Traffic Density')
                df_aux = df[['City', 'Time_taken(min)','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg(['mean', 'std'])
                df_aux.columns=['Time_mean', 'Time_std']
                df_aux = df_aux.reset_index()
                
                fig = (px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='Time_mean', 
                   color='Time_std', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['Time_std']) ))
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            with st.container():
                df_aux = df[['City', 'Time_taken(min)','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg(['mean', 'std'])
                df_aux.columns=['Time_mean', 'Time_std']
                df_aux = df_aux.reset_index()
                st.dataframe(df_aux, use_container_width=True)
        
        st.markdown("""---""")

with tab2:
    pass
    


with tab3:
    pass