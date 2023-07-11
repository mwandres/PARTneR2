
function  pintaSP_polares(f,teta,Sp,colores)



% colores=load(colores);
% colores=load(colores);

% tet=teta;
% pos=find(tet>180);
% tet(pos)=tet(pos)-360;
% [p,n]=sort(tet(:,1));
% tet=tet(n,:);
% Sp2=Sp(n,:);
% 
% teta2=[0];
% [f2,teta2]=meshgrid(f(1,:),teta2);
% Sp22=griddata(f,tet,Sp2,f2,teta2);
% 
% 
% Sp=[Sp22;Sp;Sp22];
% 
% teta=[teta(1,:).*0;teta;ones(1,length(teta(1,:))).*360];
% f=[f(1:2,:);f];
% 
% teta=teta.*pi./180;
% teta=90.*pi./180-teta;
% pos=find(teta<0);
% teta(pos)=2.*pi+teta(pos);
% pos=find(teta>2.*pi);
% teta(pos)=2.*pi-teta(pos);


% pos=find(f>0.33);
% f(pos)=NaN;teta(pos)=NaN;Sp(pos)=NaN;




[x,y,z]=pol2cart(teta,f,Sp);
% pos=find(Sp<0.1);
% Sp(pos)=NaN;
% figure;
% shading flat
% caxis([-5 5])

 
% interpolate data to a fine mesh to produce smooth grid lines
Rmin=1;%min(f(1,:));
Rmax=26;
Tmin=0; Tmax=2*pi;
N = 360;                                          % new grid size
m2 = 45; %abs(fix(N/max(1,azmgrid)));                   % angular grid spacing
r2 = 24; %abs(fix(N/max(1,13+1)));                 % radial  grid spacing
rho2  = linspace(Rmin,Rmax,N+1);                   % radius  vector
ang2 = linspace(Tmin,Tmax,N+1);                   % angle   vector
[theta2,rad] = meshgrid(ang2,rho2);                 % create polar grid
T=zeros(length(ang2),length(rho2)); 
%T = interp2(xx,yy,Zp,theta,rad,p.interpmethod);   % interpolate to grid
[xi,yi,zi] = pol2cart(theta2,rad,T);               % convert     to Cartesian
contourf(x,y,z,[min(min(z)):(max(max(z))-min(min(z)))/100:max(max(z))],'linestyle','none')
alpha(0.5)
shading flat;
lim=max(abs([min(z) max(z)]));
axis equal
axis off  
colormap(colores)
hold on
k=1;
marcas=[90 45 0 315 270 225 180 135 90];
% draw radial grid lines in azimuthal direction (meridians)
xr = xi(k:end,1:m2:end);
yr = yi(k:end,1:m2:end);
zr = zi(k:end,1:m2:end);
[mr,nr]=size(xr);
for kk=1:1:nr
    %plot3(xr(:,kk),yr(:,kk),zr(:,kk),'--k','LineWidth',1);     % plot grid lines
    plot(xr(:,kk),yr(:,kk),'-','LineWidth',2,'color',[.7 .7 .7]); 
    text(xr(end,kk)*1.2,yr(end,kk)*1.2,[num2str(marcas(kk)),' $^{\circ}$'],'fontweight','bold',...
             'horizontalalignment','center',...
             'handlevisibility','off','fontsize',9,'interpreter','latex');
   hold on
end
hold on

% draw azimuthal grid lines in radial direction (concentric arcs)
xm = xi((k+r2):r2:end,:);
ym = yi((k+r2):r2:end,:);
zm = zi((k+r2):r2:end,:);
[mm,nn]=size(xm);
c72 = cos(72*pi/180);
s72 = sin(72*pi/180);
tt=[Rmax./mm+Rmin:Rmax./mm:Rmax+Rmax./mm];

for kk=1:2:mm
    %plot3(xm(kk,:)',ym(kk,:)',zm(kk,:)','--k','LineWidth',0.5);  % plot grid lines
    plot(xm(kk,:)',ym(kk,:)','-','LineWidth',2,'color',[.7 .7 .7]);
    hold on;
    text((tt(kk).*c72),tt(kk).*s72, ...
            ['  ' num2str(round(tt(kk))) ' s' ],'fontweight','bold','color','k','verticalalignment','bottom',...
                      'handlevisibility','on','fontsize',8 ,'Interpreter','latex')
                  
end


% colorbar 
% caxis([0 0.05])
% caxis([-15 0 ])
% caxis([0 lim])
% colorbar('ytick',round([min(min(z)):(max(max(z))-min(min(z)))./5:max(max(z))].*10)./10,...
% 'yticklabel',round([min(min(z)):(max(max(z))-min(min(z)))./5:max(max(z))].*10)./10,...
%     'fontweight','bold','fontsize',9)


