# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:01:07 2023

@author: moritzw
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:27:04 2023
Script to generate fort.19 files
@author: moritzw
"""
import numpy as np
import pandas as pd
import os
import pyTMD
from adcircpy import AdcircMesh
import datetime as dt
import matplotlib.dates as mdates
import shutil

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
    #lat = y.copy()
    lat = np.zeros(np.shape(y))
    for i in range(len(y)):
        #lat = lat.replace(lat[i][:], int(lat[i][0:-1])/10)
        lat[i] = int(y[i][0:-1])/10
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

def generate_fort22_file(wind_in,pathres):
# wind_in = 'F:/Adcirc_SWAN/PARTneR2/BestTrack/Harold_tonga.csv'
# pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
# generate_fort22_file(wind_in,pathres)
    wind_out = pathres +'fort.22'
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
    return()

def get_start_and_end_time_from_besttrack(f22):
    besttrack = pd.read_csv(f22,header=None,delimiter=',')
    besttrack[2] = besttrack[2].astype(str)
    # Series of datetime values from Column
    times = pd.to_datetime(besttrack[2], format='%Y%m%d%H').dt.to_pydatetime()
    
    start_time = times[0]   #dt.datetime(2020,4,5,00)
    end_time = times[-1]    #dt.datetime(2020,4,10,13)
    return(start_time,end_time)
    

def generate_fort19_file(input_folder,pathres,tide_model_dir):
# input_folder = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/'
# pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
# tide_model_dir = 'F:/Adcirc_SWAN/PARTneR2'
# generate_fort19_file(input_folder,pathres,tide_model_dir)
    f22 = pathres +'fort.22'
    tide_out = pathres +'fort.19'
    grid_in = input_folder + 'fort.14'
    
    pbnd_x,pbnd_y = get_x_and_y(grid_in)
    start_time,end_time = get_start_and_end_time_from_besttrack(f22)
    end_time = end_time + dt.timedelta(hours = 1)
    tide = get_tidal_elevation_matrix(tide_model_dir,start_time,end_time,pbnd_x,pbnd_y)
    create_tide_file(tide_out,start_time,end_time,tide,pbnd_x,pbnd_y)
    return()

def change_dates_and_copy_f26(input_folder,pathres,start_time,end_time):
    with open(input_folder+"fort.26", 'r') as f:
                        filedata = f.read()
                        
    t1 = start_time.strftime('%Y%m%d.%H%M%S')
    t2 = end_time.strftime('%Y%m%d.%H%M%S')
    filedata = filedata.replace('%%dateinis%%', t1)
    filedata = filedata.replace('%%dateends%%', t2)
    
    with open(pathres+"fort.26", 'w') as fout:
        fout.write(filedata)
    return()

def change_dates_and_copy_f15(input_folder,pathres,start_time,end_time):
    #pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
    #input_folder = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/'
    with open(input_folder+"fort.15", 'r') as f:
                            filedata = f.read()
                        
    YYYY = start_time.strftime('%Y')
    MM = start_time.strftime('%m')
    DD = start_time.strftime('%d')
    HH = start_time.strftime('%H')
    delta = end_time - start_time
    DELTA_IN_DAYS = delta.days + delta.seconds/3600/24
    filedata = filedata.replace('YYYY', YYYY)
    filedata = filedata.replace('MM', MM)
    filedata = filedata.replace('DD', DD)
    filedata = filedata.replace('HH', HH)
    filedata = filedata.replace('DELTA_IN_DAYS', str(DELTA_IN_DAYS))
    
    with open(pathres+"fort.15", 'w') as fout:
            fout.write(filedata)
    return()

def copy_remaining_forcing_files_and_change_dates(input_folder,pathres):
    #pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
    #input_folder = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/'
    f22 = pathres +'fort.22'
    
    shutil.copyfile(input_folder+'fort.13', pathres+'fort.13')
    shutil.copyfile(input_folder+'fort.14', pathres+'fort.14')
    shutil.copyfile(input_folder+'swaninit', pathres+'swaninit')
    
    start_time,end_time = get_start_and_end_time_from_besttrack(f22)
    change_dates_and_copy_f26(input_folder,pathres,start_time,end_time)
    change_dates_and_copy_f15(input_folder,pathres,start_time,end_time)
    return()




