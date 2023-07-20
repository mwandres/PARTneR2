# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:27:04 2023
Script to generate fort.19 files
@author: moritzw
"""
import numpy as np
import os
import pyTMD
from adcircpy import AdcircMesh
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd
import datetime as dt

###
def get_x_and_y(grid_in):
    pmesh = AdcircMesh.open(grid_in,crs=4326)
    #pmesh = read_mesh(folder_name+"/fort.14")
    px = np.array(pmesh.x)
    py = np.array(pmesh.y)
    pbnd = pmesh.boundaries.ocean
    pbnd_val = pbnd.indexes
    pbnd_x = px[pbnd_val]
    pbnd_y = py[pbnd_val]
    return(pbnd_x,pbnd_y)

def get_tidal_elevation_matrix(tide_dir,start_time,end_time,pbnd_x,pbnd_y):
    grid_file = os.path.join(tide_dir,'TPXO8','DATA','grid_tpxo8atlas_30')## check if we can go for a newer version, others models can be used:'GOT4.8','FES2014',...
    model_file = os.path.join(tide_dir,'TPXO8','DATA','hf.tpxo8_atlas_30')
       
    model_format = 'OTIS'
    EPSG = '4326'
    TYPE = 'z'
    
    time_tide = mdates.drange(start_time,end_time,dt.timedelta(minutes=10))
    time_tmd=time_tide-mdates.date2num(np.datetime64('1992-01-01T00:00:00')) 
    
    z = np.zeros((len(pbnd_x),len(time_tmd)))
    for i in range(len(pbnd_x)):
        print(str(i+1) + ' / ' + str(len(pbnd_x)))
        ##LON,LAT
        LON = pbnd_x[i]
        LAT = pbnd_y[i]
        amp,ph,D,c = pyTMD.io.extract_constants(np.array([LON]), np.array([LAT]),
                                   grid_file,model_file,EPSG,TYPE=TYPE,METHOD='spline',GRID=model_format)
    
        #-- calculate complex phase in radians for Euler's
        cph = -1j*ph*np.pi/180.0
        #-- calculate constituent oscillation
        hc = amp*np.exp(cph)
        #-- predict tidal elevations at time 1 and infer minor corrections
        TIDE = pyTMD.predict.time_series(time_tmd, hc, c)
        MINOR = pyTMD.predict.infer_minor(time_tmd, hc, c, CORRECTIONS=model_format)
        TIDE.data[:] += MINOR.data
        z[i,:] = TIDE.data[:]
    return(z)

def create_tide_file(tide_out,start_time,end_time,tide,pbnd_x,pbnd_y):
    time_tide = mdates.drange(start_time,end_time,dt.timedelta(minutes=10))
    if os.path.exists(tide_out):
            os.remove(tide_out)
    with open(tide_out,'a') as tide_file:
        tide_file.write('%i\n' % 600)
        for i in range(len(time_tide)):
            for k in range(len(pbnd_x)):
                tide_file.write('%4.4f\n' % tide[k,i])
    return()

def generate_fort19_file(grid_in,pathres,tide_model_dir):
    f22 = pathres +'fort.22'
    tide_out = pathres +'fort.19'
    
    besttrack = pd.read_csv(f22,header=None,delimiter=',')
    besttrack[2] = besttrack[2].astype(str)
    # Series of datetime values from Column
    times = pd.to_datetime(besttrack[2], format='%Y%m%d%H').dt.to_pydatetime()
    
    start_time = times[0]   #dt.datetime(2020,4,5,00)
    end_time = times[-1]    #dt.datetime(2020,4,10,13)
    
    pbnd_x,pbnd_y = get_x_and_y(grid_in)
    tide = get_tidal_elevation_matrix(tide_model_dir,start_time,end_time,pbnd_x,pbnd_y)
    create_tide_file(tide_out,start_time,end_time,tide,pbnd_x,pbnd_y)
    return()

# grid_in = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/fort.14'
# pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
# tide_model_dir = 'F:/Adcirc_SWAN/PARTneR2'
# generate_fort19_file(grid_in,pathres,tide_model_dir)


