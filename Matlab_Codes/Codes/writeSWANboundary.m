function writeSWANboundary(time,locations,frec,theta,Efth,path_spectf);

% path_spectf = fullfile(foldername,'\Bound_sp');
fid = fopen(path_spectf, 'w');

% Frequency
fprintf(fid,'SWAN  1\n');
fprintf(fid,'TIME\n');
fprintf(fid,'%1.0f\n',1);
fprintf(fid,'LONLAT\n');
fprintf(fid,'%1.0f\n',length(locations(:,1)));
for ii=1:length(locations(:,1))
    fprintf(fid,'%5.6f %5.6f\n',locations(ii,1:2));
end
fprintf(fid,'AFREQ\n');
fprintf(fid,'%3.0f\n',length(frec));   % variable frequency number
%frec=f(1,:)';
fprintf(fid,'%6.8f\n',frec);

% direction
str=fprintf(fid,'NDIR\n');
fprintf(fid,'%3.0f\n',length(theta));   %variable directions number
fprintf(fid,'%6.6f\n',theta);

str=fprintf(fid,'QUANT\n');
fprintf(fid,'%1.0f\n',1);
str=fprintf(fid,'VaDens\n  m2/Hz/degr\n');
%str=fprintf(fid,'EnDens\n J/m2/Hz/degr\n');
fprintf(fid,'%2.2f\n',-99.00);

patron = '%8.0f';
for ii=1:length(theta)-1
    patron = [patron ' %8.0f'];
end
patron = [patron '\n'];

for J=1:length(time)
    fprintf(fid,[datestr(time(J),'yyyymmdd.HHMMSS') '\n']);
    for K=1:length(locations(:,1))
        %
        %             incfrec=frecup-freclow;
        %             inctheta=abs(diff(sort(theta)));
        %             inctheta=[inctheta;inctheta(1)];
        %             [INF,IND]=meshgrid(incfrec,inctheta);
         
        efth=Efth(:,:,J);
        %%%% cuidado con esta parte
        %[X,Y]=meshgrid(frec,theta);
        %         Y2=180+Y;
        %         Y2(Y2>360)=Y2(Y2>360)-360
        %         [kk,l]=sort(Y2(:,1));
        %         efth=efth(l,:);
        
        %             [Tp,Tm1,Tm2,Tz,Hs,Dm,Fspr,Dspr]=momentos3_vf(frec',INF,theta,IND,efth.*pi./180);
        %             disp(['Hs=',num2str(Hs),'m']);disp(['Dir=',num2str(Dm),'º'])
        %
        str=fprintf(fid,'FACTOR\n');
        fprintf(fid,'%G\n',0.000001);
        %fprintf(fid, patron, efth.*pi./180./0.000001);
        fprintf(fid, patron, efth./0.000001);
        %end
    end
end

fclose(fid);
fprintf('%s\n', path_spectf);

fprintf('\nSWAN spectrum input generated...\n');
end