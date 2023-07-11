function Sf = frequency_spectrum( freqs, hs, tp, gamma, sa, sb )
% INPUT
% freqs: vector of frequencies defining output discretization (s^-1)
% hs: significant wave height (m)
% tp: peak period (s)
%
% OPTIONAL INPUT
% gamma: peak enhancement parameter (adimensional) 
% sa: shape parameter for frequencies < peak frequency (adimensional)
% sb: shape parameter for frequencies > peak frequency (adimensional)
%
% OUTPUT
% Sf: distribution of energy for each frequency (m^2 * s)
%

if ~exist('gamma','var'); gamma = 3.3; end
if ~exist('sa','var'); sa = 0.07; end
if ~exist('sb','var'); sb = 0.09; end



fp = 1/tp;
s = nan(size(freqs));
s(freqs<=fp) = sa;
s(freqs>fp) = sb;

Agamma = 1-0.287*log(gamma);
SfPM =  5/16*hs^2./(tp^4.*freqs.^5).*exp(-1.25.*(tp.*freqs).^(-4));
peakFactor = gamma.^exp( -0.5 * ((tp*freqs-1)./s).^2 );
Sf = Agamma .* SfPM .* peakFactor;

end