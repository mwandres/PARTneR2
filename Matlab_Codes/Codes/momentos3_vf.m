function [Tp,Tm1,Tm2,Tz,Hs,Dm,Fspr,Dspr]=momentos3_vf(f1,df1,d1,dd1,S1)
% Esta funcion calcula los momentos espectrales mas usados 
% 

S1=S1+.00000000000001;

% Obtencion del periodo de pico
m5f=sum(sum(S1.^5.*f1.*df1.*dd1));
m5=sum(sum(S1.^5.*df1.*dd1));
fp=(m5f)/(m5);
Tp=1/fp;

%Obtencion de m0
m0=sum(sum(S1.*df1.*dd1));

%Obtencion de m1
m1=sum(sum(f1.*S1.*df1.*dd1));

%Obtencion de m2
m2=sum(sum(f1.^2.*S1.*df1.*dd1));

%Obtencion de m-1
m1b=sum(sum(f1.^(-1).*S1.*df1.*dd1));

% Obtencion de parametros
Tm1=m1b/m0;
Tm2=m0/m1;
Tz=(m0/m2)^.5;
Hs=4.004*m0^.5;

%Obtencion Direccion media
Dm1=[sum(sum(sin(d1*pi/180).*S1.*df1.*dd1)) sum(sum(cos(d1*pi/180).*S1.*df1.*dd1))];
Dm=180/pi*atan2(sum(Dm1(1)),sum(Dm1(2)));
if (Dm<0)
   Dm=Dm+360;
end


%Obtencion m0 * cos
m0_cos=sum(sum(S1.*cos(2.*pi.*(m2./m0).^(-1./2)*f1).*df1.*dd1));
%Obtencion m0 * sen
m0_sen=sum(sum(S1.*sin(2.*pi.*(m2./m0).^(-1./2)*f1).*df1.*dd1));

%Anchura frecuencial relativa
Fspr=sqrt(m0_cos^2+m0_sen^2)/m0;



%Dispersion direccional
EEx=sum(sum(cos(d1*pi/180).*S1.*df1.*dd1));
EEy=sum(sum(sin(d1*pi/180).*S1.*df1.*dd1));
FF=sqrt(EEx^2+EEy^2)/m0;
Dspr=sqrt(2-2*FF)*180/pi;

% DsM=(180/pi)*sqrt( 2* ( 1-sqrt((  sum(sin(d1(:,1)*pi/180)'.*(sum((S1.*df1)')./m0).*dd1(:,1)')  ).^2+...
%     (  sum(cos(d1(:,1)*pi/180)'.*(sum((S1.*df1)')./m0).*dd1(:,1)')  ).^2) ) );
