function [tri,xyz,elebnd,flowbnd]=adcirc_leegrid(filename)

% read fort.14 grid files


fileID = fopen(filename);

tline = fgetl(fileID);
tline = fgetl(fileID);

kk=str2num(tline)

points=kk(2);
triangles=kk(1);

xyz=ones(points,4).*NaN;
for i=1:points;
    tline = fgetl(fileID);
    xyz(i,:)=str2num(tline);
end

tri=ones(triangles,5).*NaN;
for i=1:triangles;
    tline = fgetl(fileID);
    tri(i,:)=str2num(tline);
end

tline = fgetl(fileID);
C=strsplit(tline);
nelevsegs=str2num(C{1});
tline = fgetl(fileID);
C=strsplit(tline);
totalelenodes=str2num(C{1});


for i=1:nelevsegs;
    tline = fgetl(fileID);
    C=strsplit(tline);
    kk=str2num(C{2});
    kelenodes=kk(:,1);
    
    if length(kk)==1;
        keletype=0;
    else
        keletype=kk(:,2);
    end
    
    eles=[];
    
    for j=1:kelenodes
        
        tline = fgetl(fileID);
        eles=[eles;str2num(tline)];
    end
    
    eval([' elebnd(',num2str(i),').type=keletype'])
    eval([' elebnd(',num2str(i),').eles=eles'])
end
    
    
tline = fgetl(fileID);
C=strsplit(tline);
nflowsegs=str2num(C{1});
tline = fgetl(fileID);
C=strsplit(tline);
totalflownodes=str2num(C{1});


for i=1:nflowsegs;
    tline = fgetl(fileID);
    C=strsplit(tline);
     kflownodes=str2num(C{1});

        kflowtype=str2num(C{2});
    eles=[];
    
    for j=1:kflownodes
        
        tline = fgetl(fileID);
        eles=[eles;str2num(tline)];
    end
    
    eval([' flowbnd(',num2str(i),').type= kflowtype'])
    eval([' flowbnd(',num2str(i),').eles=eles'])
end

    





    
% plot(xyz(:,2),xyz(:,3),'.')
% trisurf(tri(:,3:5),xyz(:,2),xyz(:,3),xyz(:,4)) 
% alpha(.7)% make plot using trisurf
% view(0,90);shading interp;               % make 2D view and smooth plot
% colormap(jet);colorbar;axis equal        % include colorbar and equal axes
% hold on;




