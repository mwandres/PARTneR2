# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:27:04 2023
Script to turn ibtracs/besttrack files into fort.22 files
@author: moritzw
"""
import os
import numpy as np
import pandas as pd
###
def make_run_folder(pathres):
    if not os.path.exists(pathres):
           os.mkdir(pathres)
           print("Directory " , pathres ,  " Created ")
    else:    
           print("Directory " , pathres ,  " already exists")
    return()

def correct_x(x):
    for i in range(len(x)):
        if x[i][-1] == 'W':
            x = x.replace(x[i][:],' '+ str(1800 + (1800 -  int(x[i][0:-1]))) + 'E')
    return(x)

def get_lat_from_y(y):
    lat = y.copy()    
    for i in range(len(lat)):
        lat = lat.replace(lat[i][:], int(lat[i][0:-1])/10)
    return(lat)

def get_rmax_with_knaff(Wind,lat):
    #Knaff et al. (2016)
    r_max = 218.3784 - 1.2014*Wind + (Wind/10.9844)**2 - (Wind/35.3052)**3 - (145.5090*np.cos(np.deg2rad(lat)))
    return(r_max)

def create_wind_file(wind_out,time,y,x,Wind,Pmin,Rmax):
    if os.path.exists(wind_out):
        os.remove(wind_out)
    frmt='SH, 01,%11s,   , BEST,   0,%4s,%5s,%4s,%5s,   ,    ,    ,     ,     ,     ,     , 1013,     ,%4s,    ,    ,    ,    ,    ,    ,    ,     Unnamed,  ,   ,    ,    ,    ,    ,   0\n'
    with open(wind_out,'a') as wind_file:
        for i in range(len(time)):
            wind_file.write(frmt % (time[i],y[i],x[i],Wind[i],Pmin[i],int(Rmax[i])))
    return()

#########
wind_in = 'F:/Adcirc_SWAN/PARTneR2/BestTrack/Harold_tonga.csv'
pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
wind_out = pathres +'fort.22'
#########

make_run_folder(pathres)
besttrack = pd.read_csv(wind_in,header=None,delimiter=',')

time = besttrack[2][:]
x = besttrack[7][:]
x = correct_x(x)
y = besttrack[6]
lat = get_lat_from_y(y)

Pmin = besttrack[9]
Wind = besttrack[8]
r_max = get_rmax_with_knaff(Wind,lat)
Rmax = r_max
create_wind_file(wind_out,time,y,x,Wind,Pmin,Rmax)


