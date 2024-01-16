# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:39:26 2019

@author: jlluch
"""

import gpxpy
import numpy as np
import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

def getHR(waypoint):
    for ext in waypoint.extensions:
        for e in ext:            
            if 'hr' in e.tag:
                return int(e.text)

def getTP(waypoint):
    for ext in waypoint.extensions:
        for e in ext:            
            if 'atemp' in e.tag:
                return float(e.text)

def parsegpx(f):
    #Parse a GPX file into a list of dictoinaries.  
    #Each dict is one row of the final dataset
    
    points2 = []
    with open(f, 'r') as gpxfile:
        # print f
        gpx = gpxpy.parse(gpxfile)
        
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:                   
                    #print(point.extensions)
                    dict = {'Timestamp' : point.time.strftime('%H:%M:%S'),
                            'Latitude' : point.latitude,
                            'Longitude' : point.longitude,
                            'Elevation' : point.elevation,
                            'HR' : getHR(point),
                            'TP' : getTP(point),
                            'Min': float(point.time.hour*60+point.time.minute+(point.time.second)/60)
                    }
                    points2.append(dict)
    return points2   

INDIR = ''
files = os.listdir(INDIR)

for f in files:
#Parse the gpx files into a pandas dataframe
    df = pd.DataFrame(parsegpx(f))
    df.to_csv(f.split(".")[0]+'.csv',header=True, index=False)
