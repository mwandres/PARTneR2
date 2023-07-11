function process_subdomain_wave_bnd_cons_spec(folder,spec_path)




sub=dir([folder,'/PE*']);





for i=1:length(sub(:,1));

% [EToV,VX,B,opedat,boudat,title,Node_ID] = readfort14([sub(i).folder,'/',sub(i).name,'/fort.14'],1);
% 
% bndnodes=opedat.nbdv;

[fem,bnd]=read_adcirc_mesh([folder,'\fort.14']);
bndnodes=unique(bnd.elev_nodes);

textobnd=char();
if length(bndnodes)>0
textobnd=[];
texto=['BOU SIDE 1 CCW CON FILE ' '''' spec_path '''' ' 1'];
textobnd=strcat(textobnd,texto);
end

fid = fopen([sub(i).folder,'/',sub(i).name,'/fort.26'],'r');
f=fread(fid,'*char')';
fclose(fid);
f = regexprep(f,'[$]%%BOUNDSPEC%%',textobnd)


fid = fopen([sub(i).folder,'/',sub(i).name,'/fort.26'],'w');
fprintf(fid,'%s',f);
fclose(fid);
end