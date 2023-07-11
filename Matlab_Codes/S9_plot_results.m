clear all
close all
%%
addpath('F:\Adcirc_SWAN\PARTneR2\Matlab_Codes\Codes')
pathres_Runs='F:\Adcirc_SWAN\PARTneR2\Test_Runs\Test_02\';

nc_fl_zeta = 'maxele.63.nc';
nc_fl_hs = 'swan_HS_max.63.nc';
filegrid=[ 'fort.14'];%% Grid file
[fem,elebnd]=read_adcirc_mesh(filegrid);
zeta_max = ncread(nc_fl_zeta,'zeta_max');
hs_max = ncread(nc_fl_hs,'swan_HS_max');
x = ncread([ nc_fl_zeta],'x');
y = ncread([ nc_fl_zeta],'y');

%%
fsz = 12; % default font size
bgc = [1 1 1]; % default background color
figure
hold on
m_proj('Trans','lon',[min(x) max(x)],'lat',[min(y) max(y)]) ;
m_trisurf(fem.e,fem.x,fem.y,zeta_max);
ax = gca;
ax.FontSize = fsz;
ax.Color = bgc;
m_grid('FontSize',fsz);
caxis([0 1.5])
%cmap = cmocean('balance');
cmap = flipud(cbrewer('div','RdYlBu',[23]));
colormap(cmap)
c = colorbar;
ylabel(c,'Zeta_{max} (m)')
fileprint=[pathres_Runs 'zeta_max'];
print('-dpng','-r200',fileprint)

fsz = 12; % default font size
bgc = [1 1 1]; % default background color
figure
hold on
m_proj('Trans','lon',[min(x) max(x)],'lat',[min(y) max(y)]) ;
m_trisurf(fem.e,fem.x,fem.y,hs_max);
ax = gca;
ax.FontSize = fsz;
ax.Color = bgc;
m_grid('FontSize',fsz);
caxis([0 10])
%cmap = cmocean('balance');
cmap = flipud(cbrewer('div','RdYlBu',[23]));
colormap(cmap)
c = colorbar;
ylabel(c,'Hs_{max} (m)')
fileprint=[pathres_Runs 'hs_max'];
print('-dpng','-r200',fileprint)

