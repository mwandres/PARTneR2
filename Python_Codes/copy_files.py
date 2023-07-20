# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:26:08 2023

@author: moritzw
"""
import pandas as pd
import os
import datetime as dt
import shutil

def get_start_and_end_time_from_besttrack(f22):
    besttrack = pd.read_csv(f22,header=None,delimiter=',')
    besttrack[2] = besttrack[2].astype(str)
    times = pd.to_datetime(besttrack[2], format='%Y%m%d%H').dt.to_pydatetime()
    
    start_time = times[0]
    end_time = times[-1]
    return(start_time,end_time)

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
    with open(input_folder+"fort.15", 'r') as f:
                            filedata = f.read()
                        
    YYYY = start_time.strftime('%Y')
    MM = start_time.strftime('%m')
    DD = start_time.strftime('%d')
    HH = start_time.strftime('%H')
    
    filedata = filedata.replace('YYYY', YYYY)
    filedata = filedata.replace('MM', MM)
    filedata = filedata.replace('DD', DD)
    filedata = filedata.replace('HH', HH)
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

