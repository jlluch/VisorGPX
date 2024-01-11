
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


APP_TITLE = 'Visor GPX'
APP_SUB_TITLE = 'Autor: Xavi Lluch - ai2 - UPV.    Twitter:  [@xavi_runner](https://twitter.com/xavi_runner)'

csv = ['1997571669.csv',
'1996979097.csv',
'1996151217.csv',
'1997704070.csv',
'1996085363.csv',
'1996405462.csv',
'1996175430.csv',
'1995962014.csv',
'1996197502.csv',
'1996796402.csv',
'1996483831.csv',
'1996196314.csv',
'1995875621.csv',
'1996062223.csv',
'1995937238.csv',
'1997661622.csv',
'1996075609.csv',
'1995918514.csv',
'1997259624.csv',
'1995995497.csv',
'1996180102.csv',
'1996152695.csv',
'1995988191.csv',
'1996220702.csv',
'1996169465.csv',
'1997757965.csv',
'1996466891.csv',
'1996460825.csv',
'1996396372.csv',
'1996120428.csv',
'1996868383.csv',
'1996502000.csv',
'1996302788.csv',
'1996369565.csv',
'1996011139.csv',
'1996224988.csv',
'1996412468.csv',
'1995929288.csv',
'1997580628.csv',
'1995972541.csv',
'1996109723.csv',
'1996091709.csv',
'1996295001.csv',
'1996654943.csv',
'1996072719.csv',
'1996212600.csv',
'1996102480.csv',
'1995983814.csv',
'1997006847.csv',
'1995925866.csv',
'1996187113.csv',
'1996687198.csv',
'1996220572.csv',
'1996054710.csv',
'1996259577.csv',
'1997145637.csv',
'1996611917.csv',
'1996176733.csv',
'1996160651.csv',
'1996008643.csv',
'1996161923.csv',
'1996331264.csv',
'1996762623.csv',
'1996041942.csv',
'1997058838.csv',
'1996291944.csv',
'1996191232.csv',
'1996138507.csv',
'1996260652.csv',
'1996536911.csv',
'1997884599.csv',
'1996964512.csv',
'1997187623.csv',
'1996340690.csv',
'1996139892.csv',
'1996497256.csv',
'1996416707.csv',
'1996247135.csv',
'1997616991.csv',
'1996136230.csv',
'1996046221.csv',
'1996725977.csv',
'1996422556.csv',
'1996056367.csv',
'1996203726.csv',
'1995943659.csv',
'1996254514.csv',
'1996910865.csv',
'1996156003.csv',
'1996003319.csv',
'1996172573.csv',
'1996923567.csv',
'1996399766.csv',
'1996190874.csv',
'1996189662.csv',
'1997235903.csv',
'1996309576.csv',
'1996011082.csv',
'1996156626.csv',
'1996618542.csv',
'1996394025.csv',
'1996266338.csv',
'1997652825.csv',
'1996620952.csv',
'1995992605.csv']

file = '1997571669.csv'

@st.cache_data() 
def loadFile(f):
    path     = r"https://upvedues-my.sharepoint.com/:f:/g/personal/jlluch_upv_edu_es/Em7EhjyeJRpJm3NmoeGYguYBbs1iBJcf7xvInFvTNsX9Rg?e=9FFXpB/"
    df = pd.read_csv(path+f)
        
    #columnas: Elevation	HR	Latitude	Longitude	Minutes	Tempature	Timestamp	Distance	Time_Dif	TimeDif	cumDistance
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric('Puntos', str(len(df)))
    with col2:
        st.metric('Tiempo', str(df.loc[len(df)-1,'Timestamp']))
    with col3:
        st.metric('Distancia', str(round(df.loc[len(df)-1,'cumDistance'],2))+' km') 

    #Ordena df por Distance, de mayor a menor, selecciona las 10 primeras filas, me quedo con Latitude y Longitude y hago una list zip
    df2 = df.sort_values(by=['Distance'], ascending=False).head(10)[['Latitude','Longitude','Distance']]

    st.sidebar.markdown('**Distancias**')
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric('Mínimo', str(round(df.Distance.min()*1000,3))+' m')
    with col2:        
        st.metric('Medio', str(round(df.Distance.mean()*1000,2))+' m')
    with col3:
        st.metric('Máximo', str(round(df.Distance.max()*1000,1))+' m')
    
    #esctibe en el sidebar un enlace a la actividad en Strava
    st.sidebar.markdown('**Enlace a la actividad en Strava**')
    st.sidebar.markdown('https://www.strava.com/activities/'+str(f[:-4]))
    return df, df2

def display_file_filter():    
    f = st.sidebar.selectbox('Fichero', csv, index=0, key='selectFile')
    return f


st.set_page_config(page_title=APP_TITLE,layout="wide")
st.title(APP_TITLE)

file = display_file_filter()

df, df2 = loadFile(file)

st.caption(APP_SUB_TITLE+'\n'+file)


latMap = df.Latitude.mean()
lonMap = df.Longitude.mean()

m = folium.Map(location=[latMap, lonMap], zoom_start=14,attr='LOL',max_bounds=True)

folium.PolyLine(list(zip(df['Latitude'],df['Longitude']))).add_to(m)
points = list(zip(df2['Latitude'],df2['Longitude']))
#Extrae como lista los valores de la columna Distance, multiplica por 1000 y redondea a 0 decimales y convierte a texto
text = list(map(str, list(map(lambda x: round(x, 0), df2['Distance']*1000))))
# Escribir la lista de textos en el sidebar
st.sidebar.markdown('**Distancias máximas**')
for t in text:
    st.sidebar.markdown(t+' m')
#Añade una marca en cada punto de la lista points, incluye en la marca el valor de la lista text
for point in points:
    if point == points[0]:
        folium.Marker(location=point,icon=folium.Icon(color="red"), popup=text[points.index(point)]).add_to(m)
    else:
        folium.Marker(location=point,icon=folium.Icon(color="blue"), popup=text[points.index(point)]).add_to(m)

folium_static(m, width=1280, height=1080)