# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 09:36:04 2023

@author: moritzw
"""
from make_forcings import generate_fort22_file, generate_fort19_file, copy_remaining_forcing_files_and_change_dates
from run_model import run_model
from process_output import store_output_at_point_locations, plot_and_save_figures

pathres='F:/Adcirc_SWAN/PARTneR2/Test_Runs/Rene_Test_SATO/'
cygfolder = '/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Rene_Test_SATO'

wind_in = 'F:/Adcirc_SWAN/PARTneR2/BestTrack/tc_rene.csv'
nproc = 28

#####
input_folder = 'F:/Adcirc_SWAN/PARTneR2/input_files_SATO/'
tide_model_dir = 'F:/Adcirc_SWAN/PARTneR2'
output_locations_csv1 = input_folder + 'TO.csv'
outfilename1 = 'TO_results.csv'
output_locations_csv2 = input_folder + 'SA.csv'
outfilename2 = 'SA_results.csv'
#####

generate_fort22_file(wind_in,pathres)
generate_fort19_file(input_folder,pathres,tide_model_dir)
copy_remaining_forcing_files_and_change_dates(input_folder,pathres)
run_model(nproc,pathres,cygfolder)

store_output_at_point_locations(pathres,input_folder,output_locations_csv1,outfilename1)
store_output_at_point_locations(pathres,input_folder,output_locations_csv2,outfilename2)
plot_and_save_figures(pathres)

