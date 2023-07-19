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
###

grid_in = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/fort.14'
pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
tide_out = pathres +'fort.19'
tide_dir = 'F:/Adcirc_SWAN/PARTneR2'

start_time = dt.datetime(2020,4,5,00)
end_time = dt.datetime(2020,4,10,13)

pbnd_x,pbnd_y = get_x_and_y(grid_in)
tide = get_tidal_elevation_matrix(tide_dir,start_time,end_time,pbnd_x,pbnd_y)
create_tide_file(tide_out,start_time,end_time,tide,pbnd_x,pbnd_y)



        
#         for i=1:length(time);
#     for k=1:npoints;
#         fprintf(fileID,'%4.4f\n',[tide(k,i)]);
# #######


# filegrid=[pathres 'fort.14'];%% Grid file
# [tri,xyz,elebnd,flowbnd]=adcirc_leegrid(filegrid);

# time=[datenum('5-April-2020 00:00:00'):1/24/6:datenum('10-Apr-2020 13:00:00')];
# bnd=vertcat(elebnd.eles);
# tide=ones(length(bnd),length(time));


# for i=1:length(bnd)
#     lon=xyz(bnd(i),2);
#     lat=xyz(bnd(i),3);
#     dates=[min(time):1/24/6:max(time)];
#     [z,conList]=tmd_tide_pred('C:\Users\moritzw\OneDrive - SPC\Documents\MATLAB\TMD_Matlab_Toolbox_v2.5\TMD_Matlab_Toolbox_v2.5\TMD\DATA\Model_atlas',dates,lat,lon,'z');
#     tide(i,:)=z;
# end

# filename=[pathres 'fort.19'];
# name='TPOX8';
# fileID = fopen(filename,'w');
# npoints=length(bnd);
# fprintf(fileID,'%i\n',[600]);

# for i=1:length(time);
#     for k=1:npoints;
#         fprintf(fileID,'%4.4f\n',[tide(k,i)]);
#     end
# end
# fclose(fileID);