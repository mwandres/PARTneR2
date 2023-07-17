clear all;close all;
%%
% addpath('D:\Tools\TMD_Matlab_Toolbox_v2.5\TMD');
addpath('F:\Adcirc_SWAN\PARTneR2\Matlab_Codes\Codes\');

pathres='F:\Adcirc_SWAN\PARTneR2\Test_Runs\Test_05\';
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