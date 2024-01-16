# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 17:21:08 2024

@author: jlluch
"""

import pandas as pd
import os
import glob
import math

csv_list = ['1997571669.csv',
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

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia haversine entre dos puntos dados por sus coordenadas de latitud y longitud.

    Parameters:
    lat1 (float): Latitud del primer punto en grados.
    lon1 (float): Longitud del primer punto en grados.
    lat2 (float): Latitud del segundo punto en grados.
    lon2 (float): Longitud del segundo punto en grados.

    Returns:
    float: Distancia en kilómetros entre los dos puntos.
    """
    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Convertir las coordenadas de grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencias en las coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia en kilómetros
    distance = R * c

    return distance

path     = r"C:\Users\xavi8\OneDrive - UPV\BackUP\GPX\CSV\\"
# csv_list = [os.path.basename(x) for x in glob.glob(path+ '*.csv')]
finalresult = []
col = ['file','lines', 'maxDist','minDist','meanDist','difDist','sumDist','maxTime','minTime','meanTime','difTime','sumTime']
for f in csv_list:
    df = pd.read_csv(path+f, sep=';', decimal=',')
    #Elevation	HR	Latitude	Longitude	Minutes	Tempature	Timestamp
    # Agregar columnas Distance y Time_Difference
    df['Distance'] = 0.0
    df['Time_Dif'] = 0
    
    # Calcular la distancia y la diferencia de tiempo
    for i in range(len(df) - 1):
        lat1, lon1 = df.loc[i, ['Latitude', 'Longitude']]
        lat2, lon2 = df.loc[i + 1, ['Latitude', 'Longitude']]
        
        # Calcular la distancia utilizando la función haversine_distance
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        # Calcular la diferencia de tiempo
        time_difference = df.loc[i + 1, 'Minutes'] - df.loc[i, 'Minutes']
    
        # Asignar los resultados a las columnas correspondientes
        df.loc[i + 1, 'Distance'] = distance
        df.loc[i + 1, 'TimeDif'] = time_difference
    df['cumDistance'] = df.Distance.cumsum()    
    df.to_csv(path+'OL\\'+f,index=False)    
    print(f)
    # new_row = [f]
    # new_row.append(len(df))
    # new_row.append(df.Distance.max())
    # new_row.append(df.Distance.min())
    # new_row.append(df.Distance.mean())
    # new_row.append(df.Distance.max()-df.Distance.min())
    # new_row.append(df.Distance.sum())
    # new_row.append(df.TimeDif.max())
    # new_row.append(df.TimeDif.min())
    # new_row.append(df.TimeDif.mean())
    # new_row.append(df.TimeDif.max()-df.TimeDif.min())
    # new_row.append(df.loc[len(df)-1,'Minutes'])
    # finalresult.append(new_row)

# df_results = pd.DataFrame(finalresult, columns=col) 
# df_results.to_csv('DistTime.csv', index=False)



    