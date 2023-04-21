import pandas as pd
import numpy as np
from haversine import haversine
import plotly.express as px
import folium 
from streamlit_folium import folium_static


### ----------------------------------------------------------------
### Funcoes do Curry Indian Food
### ----------------------------------------------------------------

def clean_df( df ):

    """
    Esta função é responsável por limpar o dataframe:
        1. Converter os dados para seus tipos corretos
        2. Retirar linhas com NaN 
        3. Converter a coluna de datas de str para date
        4. Retirar espaços dos str
        5. Adicionar a coluna distância de entrega

        Input: Dataframe
        Output: Dataframe
    """

    # 1. Converte os dados da coluna Delivery_person_Age de str para int
    dados_selecionados = (df["Delivery_person_Age"] != 'NaN ') 
    df = df.loc[dados_selecionados,:] # retirar os 'NaN ' de "Delivery_person_Age"
    df["Delivery_person_Age"] = df["Delivery_person_Age"].astype('int64')

    # 2. Converte os dados da coluna Delivery_person_Ratings de str para float
    df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].astype('float64')

    # 3. Converte os dados da coluna Order_Date de str para datetime
    df["Order_Date"] = pd.to_datetime(df["Order_Date"],dayfirst=True,format='%d-%m-%Y')

    # 4. Converte os dados da coluna multiple_deliveries de str para int
    dados_selecionados = (df["multiple_deliveries"] != 'NaN ') 
    df = df.loc[dados_selecionados,:] # retirar os 'NaN ' de "multiple_deliveries"
    df["multiple_deliveries"] = df["multiple_deliveries"].astype('int64')

    # 5. Retirar os 'NaN ' de "Festival"
    dados_selecionados = (df["Festival"] != 'NaN ') 
    df = df.loc[dados_selecionados,:] # retirar os 'NaN ' de "Festival"

    # 6. Corrigir os 'Yes ' para 'Yes' de "Festival"
    dados_selecionados = (df["Festival"] == 'Yes ')
    df.loc[dados_selecionados,"Festival"] = 'Yes' # corrigir os 'Yes ' de "Festival"

    # 7. Corrigir os 'XXXXXX ' para 'XXXXXX' de "ID"
    df["ID"] = df["ID"].map(lambda x: x.split()[0])

    # 8. Corrigir os 'XXXXXX ' para 'XXXXXX' de "Delivery_person_ID"
    df["Delivery_person_ID"] = df["Delivery_person_ID"].map(lambda x: x.split()[0])

    # 9. Tratar numero de "Delivery_person_ID" para ficar somente o nome
    df["Delivery_person_Name"] = df["Delivery_person_ID"].map(lambda x: x[:(len(x)-7)])

    # 10. Corrigir os 'condition XXXX' para 'XXXX' de 'Weatherconditions'
    df['Weatherconditions'] = df['Weatherconditions'].map(lambda x: x.split()[1])

    # 11. Retirar os 'NaN' do 'Weatherconditions'
    df = df.loc[df['Weatherconditions'] != 'NaN',:] 

    # 12. Retirar os espacos das categorias de 'Road_traffic_density'
    df['Road_traffic_density'] = df['Road_traffic_density'].map(lambda x: x.split()[0])

    # 13. Retirar os espacos das categorias de 'City'
    df['City'] = df['City'].map(lambda x: x.split()[0])

    # 14. Retirar os 'NaN' de 'City'
    df = df.loc[df['City'] != 'NaN',:] 

    # 15. Retirar os espacos das categorias de 'Type_of_vehicle'
    df['Type_of_vehicle'] = df['Type_of_vehicle'].map(lambda x: x.split()[0])

    # 16. Retirar os espacos das categorias de 'Type_of_vehicle'
    df['Type_of_order'] = df['Type_of_order'].map(lambda x: x.split()[0])

    # 17. Retirar o termo (min) do 'Time_taken(min)'
    df['Time_taken(min)'] = df['Time_taken(min)'].map(lambda x: int(x.split('(min) ')[1]))

    # 18. Adicionar a coluna 'Week_of_year'
    df['Week_of_year'] = df['Order_Date'].dt.strftime('%U')

    # 19. Adicionar a coluna 'Delivery_distance'
    df['Delivery_distance'] = df.loc[:,['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']].apply(
        lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1)

    return df

# Grafico de pizza dos pedidos pelas condicoes de transito
def pie_ID_RoadTraffic(df):

    df_aux = df[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['Order_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie(df_aux, names='Road_traffic_density', values='Order_perc')

    return fig


# Grafico de pedidos pela condicao de transito e pela cidade
def scatter_ID_Road_City(df):
    df_aux = df[['ID', 'Road_traffic_density', 'City' ]]. groupby([ 'City','Road_traffic_density']).count().reset_index()

    fig = px.scatter(df_aux, y='Road_traffic_density', x='City', size='ID')
    return fig


# Grafico de numero de pedidos medio por semana
def line_ordershare_week(df):
    df_aux = df[['ID', 'Delivery_person_ID', 'Week_of_year']].groupby('Week_of_year').agg({'Delivery_person_ID': 'nunique', 'ID': 'count'}).reset_index()
    df_aux['Order_per_Person_per_Week'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='Week_of_year', y='Order_per_Person_per_Week')

    return fig

# Mapa com os pedidos 
def map_order(df):
    df_aux = df[['City','Delivery_location_latitude', 'Delivery_location_longitude', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    map_india = folium.Map(location=[df_aux['Delivery_location_latitude'].median(), df_aux['Delivery_location_longitude'].median()],zoom_start=7,zoom_control=False) #, width=1400, height=500

    for _, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], popup=location_info['Road_traffic_density']).add_to(map_india)

    folium_static(map_india, width=800, height=400)