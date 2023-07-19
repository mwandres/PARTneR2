# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:27:04 2023
Script to generate fort.19 files
@author: moritzw
"""

import pyTMD
# from pyTMD.infer_minor_corrections import infer_minor_corrections
# from pyTMD.predict_tidal_ts import predict_tidal_ts
# from pyTMD.read_tide_model import extract_tidal_constants
from adcircpy import AdcircMesh
import datetime as dt
import matplotlib.dates as mdates


grid_in = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/fort.14'
pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_06_all_py/'
tide_out = pathres +'fort.19'

tide_dir = 'F:/Adcirc_SWAN/PARTneR2'

pmesh = AdcircMesh.open(grid_in,crs=4326)
#pmesh = read_mesh(folder_name+"/fort.14")
px = np.array(pmesh.x)
py = np.array(pmesh.y)
pbnd = pmesh.boundaries.ocean
pbnd_val = pbnd.indexes
pbnd_x = px[pbnd_val]
pbnd_y = py[pbnd_val]

grid_file = os.path.join(tide_dir,'TPXO8','DATA','grid_tpxo8atlas_30')## check if we can go for a newer version, others models can be used:'GOT4.8','FES2014',...
model_file = os.path.join(tide_dir,'TPXO8','DATA','hf.tpxo8_atlas_30')
   
model_format = 'OTIS'
EPSG = '4326'
TYPE = 'z'


start = dt.datetime(2020,4,7,00)
then = start + dt.timedelta(days=9.5,minutes=1)
time_tide = mdates.drange(start,then,dt.timedelta(minutes=10))
# date_time = pd.to_datetime(mdates.num2date(time_tide))
# date_time_hourly = pd.to_datetime(mdates.num2date(time_tide_hourly))
time_tmd=time_tide-mdates.date2num(np.datetime64('1992-01-01T00:00:00')) 

for i in range(5):#len(pbnd_x)):
    ##LON,LAT
    LON = pbnd_x[i]
    LAT = pbnd_y[i]
    
    pyTMD.io.extract_constants(np.array([LON]), np.array([LAT]),
                               grid_file,model_file,EPSG,TYPE=TYPE,METHOD='spline',GRID=model_format)
    
    pyTMD.predict.time_series(

    amp,ph,D,c = extract_tidal_constants(np.array([LON]), np.array([LAT]),
                grid_file,model_file,EPSG,TYPE=TYPE,METHOD='spline',GRID=model_format)
    
    deltat = np.zeros_like(time_tide)
    
    # deltat_hourly = np.zeros_like(time_tide_hourly)
    #-- calculate complex phase in radians for Euler's
    cph = -1j*ph*np.pi/180.0
    #-- calculate constituent oscillation
    hc = amp*np.exp(cph)

    #-- predict tidal elevations at time 1 and infer minor corrections
    #-- convert to centimeters
    TIDE = predict_tidal_ts(time_tmd, hc, c,
        DELTAT=deltat, CORRECTIONS=model_format)*100.0
    MINOR = infer_minor_corrections(time_tmd, hc, c,
        DELTAT=deltat, CORRECTIONS=model_format)
    TIDE.data[:] += MINOR.data

    f = interp1d(time_tide,TIDE)
    TIDE_hourly = f(time_tide_hourly)
        
        
#######


filegrid=[pathres 'fort.14'];%% Grid file
[tri,xyz,elebnd,flowbnd]=adcirc_leegrid(filegrid);

time=[datenum('5-April-2020 00:00:00'):1/24/6:datenum('10-Apr-2020 13:00:00')];
bnd=vertcat(elebnd.eles);
tide=ones(length(bnd),length(time));


for i=1:length(bnd)
    lon=xyz(bnd(i),2);
    lat=xyz(bnd(i),3);
    dates=[min(time):1/24/6:max(time)];
    [z,conList]=tmd_tide_pred('C:\Users\moritzw\OneDrive - SPC\Documents\MATLAB\TMD_Matlab_Toolbox_v2.5\TMD_Matlab_Toolbox_v2.5\TMD\DATA\Model_atlas',dates,lat,lon,'z');
    tide(i,:)=z;
end

filename=[pathres 'fort.19'];
name='TPOX8';
fileID = fopen(filename,'w');
npoints=length(bnd);
fprintf(fileID,'%i\n',[600]);

for i=1:length(time);
    for k=1:npoints;
        fprintf(fileID,'%4.4f\n',[tide(k,i)]);
    end
end
fclose(fileID);