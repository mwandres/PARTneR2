function D = directional_distribution( dirs, si, th )
% INPUT
% dirs: vector of directions defining output discretization (degrees)
% si: directional spread (degrees)
% th: mean direction (degrees)
%
% OUTPUT
% D: distribution of energy for each direction (adimensional, sum(D*dth(radians))=1)
%

% NO wrapped because partitions have very small spread

theta = min(cat(3, abs(th-dirs), 360-abs(th-dirs)),[],3);
 

% s = (2./((si*pi/180).^2))-1;%% paso si a radianes, see Holthuijsen pag165
% A2 = gamma(s+1)./(gamma(s+0.5)*2*sqrt(pi));
% D = A2.*(cosd(theta/2)).^(2*s);

dth = 2*pi/length(dirs);
D = normpdf(0, theta, si);
D = D/(sum(D))/dth;
end
