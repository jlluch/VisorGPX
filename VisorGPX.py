
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:41:40 2022

@author: jlluch
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium, folium_static
from datetime import datetime
import os
import plotly.express as px


APP_TITLE = 'Visor GPX'
APP_SUB_TITLE = 'Autor: Xavi Lluch - ai2 - UPV.    Twitter:  [@xavi_runner](https://twitter.com/xavi_runner)'


file = 'VLC23Dist.csv'
path     = ""
#Creo una lista con los ficheros csv del directorio OL
# csv = os.listdir(path)
csv = ['VLC23Dist.csv','VLC23-1Dist.csv','VLC23-2Dist.csv']#,'VLC23-3Dist.csv']

@st.cache_data() 
def loadFile(f):
    df = pd.read_csv(path+f)
    #columnas: Elevation	HR	Latitude	Longitude	Minutes	Tempature	Timestamp	Distance	Time_Dif	TimeDif	cumDistance
    dfO = pd.read_csv((path+f).replace("Dist","",1))
    #Calcula el ritmo en minutos por km
    dfO['Pace'] = 0.0
    dfO['Pace'] = (dfO['TimeDif']/60) / (dfO['Distance'])

    st.sidebar.markdown('**Original**')
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric('Puntos', str(len(dfO)))
    with col2:
        st.metric('Tiempo', str(dfO.loc[len(dfO)-1,'Seconds']))
    with col3:
        st.metric('Distancia', str(round(dfO.loc[len(dfO)-1,'cumDistance'],2))+' km') 
    
    st.sidebar.markdown('**Distancias**')
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric('Mínimo', str(round(dfO.Distance.min()*1000,3))+' m')
    with col2:        
        st.metric('Medio', str(round(dfO.Distance.mean()*1000,2))+' m')
    with col3:
        st.metric('Máximo', str(round(dfO.Distance.max()*1000,1))+' m')
    
    st.sidebar.markdown('**Ajustado**')
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric('Puntos', str(len(df)))
    with col2:
        st.metric('Tiempo', str(df.loc[len(df)-1,'Seconds']))
    with col3:
        st.metric('Distancia', str(round(df.loc[len(df)-1,'cumDistance'],2))+' km') 
    
    st.sidebar.markdown('**Distancias**')
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric('Mínimo', str(round(df.Distance.min()*1000,3))+' m')
    with col2:        
        st.metric('Medio', str(round(df.Distance.mean()*1000,2))+' m')
    with col3:
        st.metric('Máximo', str(round(df.Distance.max()*1000,1))+' m')
    
    #Ordena df por Distance, de mayor a menor, selecciona las 10 primeras filas, me quedo con Latitude y Longitude y hago una list zip
    df2 = df.sort_values(by=['Distance'], ascending=False).head(10)[['Latitude','Longitude','Distance']]    
    
    #escribe en el sidebar un enlace a la actividad en Strava
    st.sidebar.markdown('**Enlace a la actividad en Strava**')
    st.sidebar.markdown('https://www.strava.com/activities/'+str(f[:-4]))
    return df, df2, dfO

def display_file_filter():    
    f = st.sidebar.selectbox('Fichero', csv, index=0, key='selectFile')
    return f


st.set_page_config(page_title=APP_TITLE,layout="wide")
st.title(APP_TITLE)

file = display_file_filter()

df, df2, dfO = loadFile(file)

st.caption(APP_SUB_TITLE+'\n'+file)


latMap = df.Latitude.mean()
lonMap = df.Longitude.mean()

m = folium.Map(location=[latMap, lonMap], zoom_start=14,attr='LOL',max_bounds=True)
#Dibuja el recorrido de la actividad en rojo
folium.PolyLine(list(zip(dfO['Latitude'],dfO['Longitude'])), color = 'red', opacity=0.5).add_to(m)


#Dibuja el recorrido ajustado y pone puntos negros en los elegidos
folium.PolyLine(list(zip(df['Latitude'],df['Longitude']))).add_to(m)
points = list(zip(df['Lat'],df['Lon']))
for point in points:
    folium.CircleMarker(location=point, color='black', fill=True, radius=2).add_to(m)

points = list(zip(df['Latitude'],df['Longitude']))
for point in points:
    folium.CircleMarker(location=point, color='brown', fill=True, radius=2).add_to(m)

points = list(zip(df2['Latitude'],df2['Longitude']))
#Extrae como lista los valores de la columna Distance, multiplica por 1000 y redondea a 0 decimales y convierte a texto
text = list(map(str, list(map(lambda x: round(x, 0), df2['Distance']*1000))))
# Escribir la lista de textos en el sidebar
st.sidebar.markdown('**Distancias máximas**')
for t in text:
    st.sidebar.markdown(t+' m')
# #Añade una marca en cada punto de la lista points, incluye en la marca el valor de la lista text
# for point in points:
#     if point == points[0]:
#         folium.Marker(location=point,icon=folium.Icon(color="red"), popup=text[points.index(point)]).add_to(m)
#     else:
#         folium.Marker(location=point,icon=folium.Icon(color="blue"), popup=text[points.index(point)]).add_to(m)

folium_static(m, width=1280, height=1080)

#Dibuja el gráfico de ritmo por distancia para el recorrido original
fig = px.line(dfO, x="cumDistance", y="Pace", title='Original')
fig.update_xaxes(title_text='Distancia (km)')
fig.update_yaxes(title_text='Ritmo (min/km)')
st.plotly_chart(fig, use_container_width=True)

#Dibuja el gráfico de ritmo por distancia para el recorrido ajustado
fig = px.line(df, x="cumDistance", y="Pace", title='Ajustado')
fig.update_xaxes(title_text='Distancia (km)')
fig.update_yaxes(title_text='Ritmo (min/km)')
st.plotly_chart(fig, use_container_width=True)
