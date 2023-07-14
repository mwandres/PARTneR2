clear all;close all;
%%
% addpath('D:\Tools\TMD_Matlab_Toolbox_v2.5\TMD');
addpath('F:\Adcirc_SWAN\PARTneR2\Matlab_Codes\Codes\');
pathres='F:\Adcirc_SWAN\PARTneR2\Test_Runs\Test_04\';
filegrid=[pathres 'fort.14'];%% Grid file
wind_in = ['F:\Adcirc_SWAN\PARTneR2\BestTrack\Harold_tonga.txt'];
wind_out = [pathres 'fort.22'];
[tri,xyz,elebnd,flowbnd]=adcirc_leegrid(filegrid);
%%
besttrack = readtable(wind_in);
time = datenum(num2str(besttrack.Var3),'yyyymmddhh');
x = besttrack.Var8;
y = besttrack.Var7;
for i = 1:length(y)
    lat(i,1) = str2num(y{i}(1:3))/10;
end
Pmin = besttrack.Var10;
Wind = besttrack.Var9;
r_max = 218.3784 - 1.2014*Wind + (Wind./10.9844).^2 - (Wind./35.3052).^3 - (145.5090*cos(deg2rad(lat)));
Rmax = r_max;
%Rmax = besttrack.Var20;
filename = wind_out;
HURDATformat_gentrack(time,x,y,Pmin,Wind,Rmax,filename)
%%
function HURDATformat_gentrack(time,x,y,Pmin,Wind,Rmax,filename)
fileID = fopen(filename,'w');
for i=1:length(x)
    format='SH, 01,%11s,   , BEST,   0, %4s, %5s,%4s,%5s,   ,    ,    ,     ,     ,     ,     , 1013,     ,%4s,    ,    ,    ,    ,    ,    ,    ,     Unnamed,  ,   ,    ,    ,    ,    ,   0\n';
    fprintf(fileID,format, datestr(time(i),'yyyymmddhh'),y{i},x{i},num2str(round(Wind(i))),num2str(round(Pmin(i))),num2str(round(Rmax(i))));
%    fprintf(fileID,format, datestr(time(i),'yyyymmddhh'),num2str(round(y(i).*10)),num2str(round(x(i).*10)),num2str(round(Wind(i))),num2str(round(Pmin(i))),num2str(round(Rmax(i))));
end
fclose(fileID);
end
% 
% time=[datenum('11-Feb-2010 12:00:00'):1/24/6:datenum('18-Feb-2010 19:00:00')];
% bnd=vertcat(elebnd.eles);
% tide=ones(length(bnd),length(time));
% 
% for i=1:length(bnd)
%     lon=xyz(bnd(i),2);
%     lat=xyz(bnd(i),3);
%     dates=[min(time):1/24/6:max(time)];
%     [z,conList]=tmd_tide_pred('C:\Users\moritzw\OneDrive - SPC\Documents\MATLAB\TMD_Matlab_Toolbox_v2.5\TMD_Matlab_Toolbox_v2.5\TMD\DATA\Model_atlas',dates,lat,lon,'z');
%     tide(i,:)=z;
% end
% 
% filename=[pathres 'fort.19'];
% name='TPOX8';
% fileID = fopen(filename,'w');
% npoints=length(bnd);
% fprintf(fileID,'%i\n',[600]);
% 
% for i=1:length(time);
%     for k=1:npoints;
%         fprintf(fileID,'%4.4f\n',[tide(k,i)]);
%     end
% end
% fclose(fileID);