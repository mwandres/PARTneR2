clear all;close all;

pathres='F:\Adcirc_SWAN\PARTneR2\Test_Runs\Test_05_b_no_Knaff\';
cd(pathres);

fid  = fopen('partmesh.sh','w');
fprintf(fid,'%s','/cygdrive/c/adcirc_v54.02/build/adcprep.exe --np 28 --partmesh');
fprintf(fid,'\n');
fprintf(fid,'%s','/cygdrive/c/adcirc_v54.02/build/adcprep.exe --np 28 --prepall');
fclose(fid);

system(['C:\cygwin64\bin\bash --login -c   "cd ','/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Test_05_b_no_Knaff','; ./partmesh.sh"'])
system(['C:\cygwin64\bin\bash --login -c   "cd ','/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Test_05_b_no_Knaff','; mpirun -np 28 /cygdrive/f/Adcirc_SWAN/PARTneR2/ADCIRC55/ADCIRC55/padcswan_SH.exe"'])

system('taskkill /F /IM padcswan_SH.exe')
% system('rm -r PE*')
