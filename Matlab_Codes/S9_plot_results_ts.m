clear all
close all
%%
addpath('F:\Adcirc_SWAN\PARTneR2\Matlab_Codes\Codes')
pathres_Runs='F:\Adcirc_SWAN\PARTneR2\Test_Runs\Test_04\';

nc_fl_zeta = [pathres_Runs 'fort.63.nc'];
nc_fl_hs = [pathres_Runs 'swan_HS.63.nc'];
filegrid=[pathres_Runs 'fort.14'];%% Grid file
[fem,elebnd]=read_adcirc_mesh(filegrid);
zeta_max = ncread(nc_fl_zeta,'zeta');
hs_max = ncread(nc_fl_hs,'swan_HS');
x = ncread([ nc_fl_zeta],'x');
y = ncread([ nc_fl_zeta],'y');
time = ncread([nc_fl_zeta],'time');
%%
for i = 1:length(time)
fsz = 12; % default font size
bgc = [1 1 1]; % default background color
figure
hold on
m_proj('Trans','lon',[min(x) max(x)],'lat',[min(y) max(y)]) ;
m_trisurf(fem.e,fem.x,fem.y,squeeze(zeta_max(:,i)));
ax = gca;
ax.FontSize = fsz;
ax.Color = bgc;
m_grid('FontSize',fsz);
caxis([0 1.5])
%cmap = cmocean('balance');
cmap = flipud(cbrewer('div','RdYlBu',[23]));
colormap(cmap)
c = colorbar;
title(datestr(datenum(2020,4,7,time(i)/3600,0,0)))
ylabel(c,'Zeta (m)')
fileprint=[pathres_Runs 'zeta_' num2str(i)];
print('-dpng','-r200',fileprint)

fsz = 12; % default font size
bgc = [1 1 1]; % default background color
figure
hold on
m_proj('Trans','lon',[min(x) max(x)],'lat',[min(y) max(y)]) ;
m_trisurf(fem.e,fem.x,fem.y,squeeze(hs_max(:,i)));
ax = gca;
ax.FontSize = fsz;
ax.Color = bgc;
m_grid('FontSize',fsz);
caxis([0 10])
%cmap = cmocean('balance');
cmap = flipud(cbrewer('div','RdYlBu',[23]));
colormap(cmap)
c = colorbar;
title(datestr(datenum(2020,4,7,time(i)/3600,0,0)))
%title(num2str(time(i)/3600))
ylabel(c,'Hs (m)')
fileprint=[pathres_Runs 'hs_' num2str(i)];
print('-dpng','-r200',fileprint)
close all
end