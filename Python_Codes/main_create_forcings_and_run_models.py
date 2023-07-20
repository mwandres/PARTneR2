# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 09:36:04 2023

@author: moritzw
"""
from make_forcings import generate_fort22_file, generate_fort19_file, copy_remaining_forcing_files_and_change_dates
from run_model import run_model

pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Harold_Test/'
cygfolder = '/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Harold_Test'

wind_in = 'F:/Adcirc_SWAN/PARTneR2/BestTrack/Harold_tonga.csv'
nproc = 28

#####
input_folder = 'F:/Adcirc_SWAN/PARTneR2/Test_Runs/input_files/'
tide_model_dir = 'F:/Adcirc_SWAN/PARTneR2'

generate_fort22_file(wind_in,pathres)
generate_fort19_file(input_folder,pathres,tide_model_dir)
copy_remaining_forcing_files_and_change_dates(input_folder,pathres)
#run_model(nproc,pathres,cygfolder)