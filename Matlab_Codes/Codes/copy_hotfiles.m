function copy_hotfiles(in_folder,out_folder)
sub=dir([in_folder,'/PE*']);
% f67 = ([sub(1).folder,'\',sub(1).name,'\fort.67.nc']);
% f68 = ([sub(1).folder,'\',sub(1).name,'\fort.68.nc']);
f67 = ([in_folder,'\fort.67.nc']);
f68 = ([in_folder,'\fort.68.nc']);
copyfile(f67,out_folder)
copyfile(f68,out_folder)
for i=1:length(sub(:,1))
    s67 = ([sub(i).folder,'\',sub(i).name,'\swan.67']);
    s68 = ([sub(i).folder,'\',sub(i).name,'\swan.68']);
    copyfile(s67,[out_folder,'\',sub(i).name])
    copyfile(s68,[out_folder,'\',sub(i).name])
end
end