function process_subdomain_wave_bnd(folder,bry_folder)


[fem,bnd]=read_adcirc_mesh([folder,'\fort.14']);


bndnodesg=unique(bnd.elev_nodes);

x1g=fem.x(bndnodesg);
y1g=fem.y(bndnodesg);
% 
% fid  = fopen([folder,'boundaryIJK'],'w');
% for ii=1:length(bndnodesg)
%     texto=[' BOUN SEGMENT IJ ',num2str(bndnodesg(ii)),' VAR FILE 0 ','''','Pto_sp_',num2str(bndnodesg(ii)),'''',' 1, &']
%     fprintf(fid,'%s\n',texto);
% end
% fclose(fid);


sub=dir([folder,'/PE*']);



for i=1:length(sub(:,1));
    
    [fem,bnd]=read_adcirc_mesh([sub(i).folder,'\',sub(i).name,'\fort.14']);
 
    bndnodes=unique(bnd.elev_nodes);
    x1=fem.x(bndnodes);
    y1=fem.y(bndnodes);
    
    textobnd=char();
    if length(bndnodes)>0
        
       textobnd=[];
        for ii=1:length(bndnodes);
            
            [~,pos]=min(sqrt((x1g-x1(ii)).^2+(y1g-y1(ii)).^2));

             texto=[' BOUN SEGMENT IJ ',num2str(bndnodes(ii)),' VAR FILE 0 ','''',bry_folder, '/Pto_sp_',num2str(bndnodesg(pos)),'''',' 1, &\n'];

            if ii==length(bndnodes) & length(bndnodes)~=1;
           texto=[' BOUN SEGMENT IJ ',num2str(bndnodes(ii)),' VAR FILE 0 ','''',bry_folder, '/Pto_sp_',num2str(bndnodesg(pos)),'''',' 1'];
            end
            
            textobnd=strcat(textobnd,texto);
        end
    end
    
%     fid  = fopen([sub(i).folder,'/',sub(i).name,'/fort.26'],'r');
fid  = fopen([sub(i).folder,'\fort.26'],'r');
    f=fread(fid,'*char')';
    fclose(fid);
    f =  regexprep(f,'[$]%%BOUNDSPEC%%',textobnd)
    
    
    fid  = fopen([sub(i).folder,'/',sub(i).name,'\fort.26'],'w');
    fprintf(fid,'%s',f);
    fclose(fid);
    
end
