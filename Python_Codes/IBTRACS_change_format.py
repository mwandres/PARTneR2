# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 09:30:38 2023

@author: moritzw
"""
import pandas as pd
import numpy as np

def read_and_write_ibtracs(fl_name,tc_name,out_name):
    besttrack = pd.read_csv(fl_name,header=0,delimiter=',')
    ix = besttrack['NAME'] == tc_name
    
    outtrack = pd.DataFrame()
    outtrack[0] = besttrack['SID'][ix]
    outtrack[1] = besttrack['BASIN'][ix]
    outtrack[2] = besttrack['ISO_TIME'][ix] ###
    outtrack[2] = pd.to_datetime(outtrack[2])
    outtrack[2] = outtrack[2].dt.strftime('%Y%m%d%H')
    outtrack[3] = besttrack['NAME'][ix]
    outtrack[4] = besttrack['TRACK_TYPE'][ix]
    outtrack[5] = besttrack['NATURE'][ix]
    outtrack[6] = besttrack['LAT'][ix] ##
    outtrack[7] = besttrack['LON'][ix] ##
    outtrack[8] = besttrack['USA_WIND'][ix]
    outtrack[9] = besttrack['USA_PRES'][ix]
    outtrack[10]= besttrack['USA_RMW'][ix] #if exists
    outtrack = outtrack.reset_index(drop=True)
    lat = outtrack[6]
    for i in range(len(lat)):
        if float(lat[i]) < 0:
            hemi = 'S'
            lat[i] = float(lat[i])*-1
        else:
            hemi = 'N'
        lat[i] = float(lat[i]) * 10
        lat[i] = int(lat[i])
        outtrack[6][i] = str(lat[i])+hemi
    lon = outtrack[7]
    for i in range(len(lon)):
        lon[i] = float(lon[i])*10
        lon[i] = int(lon[i])
        outtrack[7][i] = str(lon[i])+'E'
    outtrack.to_csv(out_name,index=False,header=False)
    return()



fl_name = 'F:/Adcirc_SWAN/PARTneR2/BestTrack/ibtracs.ACTIVE.list.v04r00.csv'
tc_name = 'LOLA'
out_name = 'F:/Adcirc_SWAN/PARTneR2/BestTrack/TC_Lola_24Oct.csv'
read_and_write_ibtracs(fl_name,tc_name,out_name)


