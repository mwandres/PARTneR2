clear all;close all;

%addpath(genpath('D:\Tools\OceanMesh2D\utilities'))
%addpath('D:\Projects_SPC\Majuro\soft\Coupled_fullSp_Majuro')

pathres='F:\Adcirc_SWAN\Tonga\Test_Runs\Test_01\';



% %tic
% y1=dat(j,1);m1=dat(j,2);
% foldername=[pathres,num2str(y1),num2str(m1,'%02d')];
cd(pathres);


fid  = fopen('partmesh.sh','w');
fprintf(fid,'%s','/cygdrive/c/adcirc_v54.02/build/adcprep.exe --np 16 --partmesh');
fprintf(fid,'\n');
fprintf(fid,'%s','/cygdrive/c/adcirc_v54.02/build/adcprep.exe --np 16 --prepall');
fclose(fid);

system(['C:\cygwin64\bin\bash --login -c   "cd ','/cygdrive/f/Adcirc_SWAN/Tonga/Test_Runs/Test_01','; ./partmesh.sh"'])
%bry_folder = ['D:/Adcirc_SWAN/Funafuti_Hindcast/Waves/' num2str(y1),num2str(m1,'%02d')];
% process_subdomain_wave_bnd(foldername,bry_folder)
% if m1 ~= 1
%     in_folder=[pathres,num2str(y1),num2str(m1-1,'%02d')];
%     out_folder=foldername;
%     copy_hotfiles(in_folder,out_folder)
% end
system(['C:\cygwin64\bin\bash --login -c   "cd ','/cygdrive/f/Adcirc_SWAN/Tonga/Test_Runs/Test_01','; mpirun -np 16 /cygdrive/c/adcirc_v54.02/build/padcswan.exe"'])

system('taskkill /F /IM padcswan.exe')
% system('rm -r PE*')
%toc
