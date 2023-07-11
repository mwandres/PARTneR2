function [Hsig,Tm01] = Spec2Hs_and_Tm01(dirs,frqs,efth)
%SPEC2HS Summary of this function goes here
%   Detailed explanation goes here
% rho = 1025;
% g = 9.81;
% E2 = efth/ rho; %divide by density
% E3 = E2/ g; %divide by g 
E3 = efth;
for i = 1:length(frqs)
   spec1d_all(i) = sum(E3(i,:) * 10);
end
m0        = trapz(frqs,spec1d_all');
m1        = trapz(frqs,frqs.*spec1d_all');
Hsig = 4.*sqrt(m0);
Tm01   = m0./m1;
end

