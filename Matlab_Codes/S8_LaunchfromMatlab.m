clear all;close all;

%addpath(genpath('D:\Tools\OceanMesh2D\utilities'))
%addpath('D:\Projects_SPC\Majuro\soft\Coupled_fullSp_Majuro')

pathres='F:\Adcirc_SWAN\PARTneR2\Test_Runs\Test_04\';



% %tic
% y1=dat(j,1);m1=dat(j,2);
% foldername=[pathres,num2str(y1),num2str(m1,'%02d')];
cd(pathres);

% 
% fid  = fopen('partmesh.sh','w');
% fprintf(fid,'%s','/cygdrive/f/Adcirc_SWAN/PARTneR2/ADCIRC55/ADCIRC55/adcprep.exe --np 16 --partmesh');
% fprintf(fid,'\n');
% fprintf(fid,'%s','/cygdrive/f/Adcirc_SWAN/PARTneR2/ADCIRC55/ADCIRC55/adcprep.exe --np 16 --prepall');
% fclose(fid);


fid  = fopen('partmesh.sh','w');
fprintf(fid,'%s','/cygdrive/c/adcirc_v54.02/build/adcprep.exe --np 28 --partmesh');
fprintf(fid,'\n');
fprintf(fid,'%s','/cygdrive/c/adcirc_v54.02/build/adcprep.exe --np 28 --prepall');
fclose(fid);


system(['C:\cygwin64\bin\bash --login -c   "cd ','/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Test_02_c','; ./partmesh.sh"'])
%bry_folder = ['D:/Adcirc_SWAN/Funafuti_Hindcast/Waves/' num2str(y1),num2str(m1,'%02d')];
% process_subdomain_wave_bnd(foldername,bry_folder)
% if m1 ~= 1
%     in_folder=[pathres,num2str(y1),num2str(m1-1,'%02d')];
%     out_folder=foldername;
%     copy_hotfiles(in_folder,out_folder)
% end
system(['C:\cygwin64\bin\bash --login -c   "cd ','/cygdrive/f/Adcirc_SWAN/PARTneR2/Test_Runs/Test_04','; mpirun -np 12 /cygdrive/f/Adcirc_SWAN/PARTneR2/ADCIRC55/ADCIRC55/padcswan_SH_2.exe"'])

system('taskkill /F /IM padcswan_SH.exe')
% system('rm -r PE*')
%toc
