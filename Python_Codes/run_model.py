# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:32:25 2023

@author: moritzw
"""
import os



def run_model(nproc,pathres,cygfolder):
    os.chdir(pathres)
    os.system('C:/cygwin64/bin/bash --login -c "cd %s;  /cygdrive/c/adcirc_v54.02/build/adcprep.exe --np %s --partmesh"' %(cygfolder,str(nproc)))
    os.system('C:/cygwin64/bin/bash --login -c "cd %s;  /cygdrive/c/adcirc_v54.02/build/adcprep.exe --np %s --prepall"' %(cygfolder,str(nproc)))
    os.system('C:/cygwin64/bin/bash --login -c "cd %s; mpirun --use-hwthread-cpus -np %s /cygdrive/f/Adcirc_SWAN/PARTneR2/ADCIRC55/ADCIRC55/padcswan_SH_2"' %(cygfolder,str(nproc)))
    try: 
        os.system('taskkill /F /IM padcswan_SH_2.exe')
    except:
        print('SWAN run finished succesfully')
    
    
# nproc = 28
# pathres = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/Test_01/'
# cygfolder = '/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Test_01'
# run_model(nproc,pathres,cygfolder)