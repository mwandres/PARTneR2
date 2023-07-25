# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:27:33 2023

@author: moritzw
"""
import os
import numpy as np
import pandas as pd
import netCDF4
import math
from joblib import Parallel, delayed
import adcircpy
import matplotlib.tri as tri
from matplotlib import pyplot as plt
import cartopy.crs as ccrs

def make_results_folder(pathres):
    if not os.path.exists(pathres + '/results'):
           os.mkdir(pathres+ '/results')
           print("Directory " , pathres+ '/results' ,  " Created ")
    else:    
           print("Directory " , pathres+ '/results' ,  " already exists")
    return()

def load_zeta_and_hs_max(pathres):
    nc_fl_zeta = pathres+ 'maxele.63.nc'
    nc_fl_hs = pathres+ 'swan_HS_max.63.nc'
    nc_zeta = netCDF4.Dataset(nc_fl_zeta)
    nc_hs = netCDF4.Dataset(nc_fl_hs)
    lon = np.array(nc_zeta['x'])
    lat = np.array(nc_zeta['y'])
    zeta_max = np.array(nc_zeta['zeta_max'])
    hs_max = np.array(nc_hs['swan_HS_max'])
    return(lon,lat,zeta_max,hs_max)

def get_target_lon_and_lat(output_locations_csv):    
    output_pts = pd.read_csv(output_locations_csv,delimiter=',')
    target_lat = output_pts['lat']
    target_lon = output_pts['lon']
    return(target_lon,target_lat)

def haversine_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p)*math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
    return(12742 * math.asin(math.sqrt(hav)))

def get_indices_for_closest_lat_lon(lat,lon,target_lat,target_lon):
    posix = np.zeros(np.size(target_lon))
    for jx in range(len(target_lon)):
        dis = np.zeros(np.size(lon))
        for ix in range(len(lon)):
            dis[ix] = haversine_distance(lat[ix],lon[ix],target_lat[jx],target_lon[jx])
        pos_ix = np.where(dis == np.min(dis))
        posix[jx] = pos_ix[0][0]
        print(jx)
    return(posix)

def get_ix_of_min_dist(lon,lat,trgt_ln,trgt_lt):
    dis = np.zeros(np.size(lon))
    for ix in range(len(lon)):
        dis[ix] = haversine_distance(lat[ix],lon[ix],trgt_lt,trgt_ln)
    pos_ix = np.where(dis == np.min(dis))
    posix = pos_ix[0][0]
    return(posix)

def get_zeta_and_hs_at_point_locations(zeta_max,hs_max,posix):
    zeta_output = np.zeros(np.size(posix))
    hs_output = np.zeros(np.size(posix))
    for i in range(len(posix)):
        zeta_output[i] = zeta_max[posix[i]]
        hs_output[i] = hs_max[posix[i]]
    return(zeta_output,hs_output)

def store_output_at_point_locations(pathres,input_folder,output_locations_csv,outfilename):
# pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Harold_Test/'
# input_folder = 'F:/Adcirc_SWAN/PARTneR2/input_files/'
# output_locations_csv = input_folder + 'TO.csv'
    lon,lat,zeta_max,hs_max = load_zeta_and_hs_max(pathres)
    target_lon,target_lat = get_target_lon_and_lat(output_locations_csv)
    #posix2 = get_indices_for_closest_lat_lon(lat,lon,target_lat,target_lon) # can do in serial but it's very slow.
    posix = Parallel(n_jobs=12)(delayed(get_ix_of_min_dist)(lon,lat,target_lon[i],target_lat[i]) for i in range(len(target_lon)))
    zeta_output,hs_output = get_zeta_and_hs_at_point_locations(zeta_max,hs_max,posix)
    make_results_folder(pathres)
    df = pd.DataFrame({"lon": target_lon, "lat": target_lat, "zeta_max": zeta_output, "hs_max": hs_output})
    df.to_csv(pathres + '/results/'+outfilename,index=False)
    return()

# def plot_unswan(lon,lat,z,title,cbarlabel,vmin,vmax,cmap):
#     triang = tri.Triangulation(lon, lat)
#     f = plt.figure()
#     levels = np.linspace(vmin, vmax, 91)
#     plt.tricontourf(triang,z,levels=levels, cmap=cmap)
#     plt.title(title)
#     cb = plt.colorbar()
#     cb.set_label(cbarlabel)
#     plt.show(block=False)
#     ax = plt.gca()
#     return(f,ax)


def plot_unswan(lon,lat,z,title,cbarlabel,levels,cmap):
    triang = tri.Triangulation(lon, lat)
    fig = plt.figure(figsize=(12, 8))
    img_extent = (np.min(lon),np.max(lon),np.min(lat),np.max(lat))
    
    proj = ccrs.PlateCarree(central_longitude=180)
    ax = plt.axes(projection=proj)
    
    ax.set_extent(img_extent,crs=ccrs.PlateCarree())

    plt.title(title)
    ax.use_sticky_edges = False    
    # set a margin around the data
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.10)
    
    im = ax.tricontourf(triang, z, levels=levels, cmap=cmap, transform=ccrs.PlateCarree())
    #im = ax.tricontourf(triang, z, cmap=cmap, transform=ccrs.PlateCarree())

    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.gridlines(crs=ccrs.PlateCarree(central_longitude=180), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
    cb = fig.colorbar(im)
    cb.set_label(cbarlabel)
    return(fig,ax)

def plot_and_save_figures(pathres):
    lon,lat,zeta_max,hs_max = load_zeta_and_hs_max(pathres)
    levels = np.linspace(min(zeta_max), max(zeta_max), 91)
    fig,ax = plot_unswan(lon,lat,zeta_max,'zeta_max','zeta_max',levels,"gist_ncar")
    plt.savefig(pathres+'results/zeta_max.png')
    plt.close(fig)
    levels = np.linspace(min(hs_max), max(hs_max), 91)
    fig,ax = plot_unswan(lon,lat,hs_max,'hs_max','hs_max',levels,"gist_ncar")
    plt.savefig(pathres+'results/hs_max.png')
    plt.close(fig)
    return()