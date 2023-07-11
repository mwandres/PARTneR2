function [Sthf, freqsMatrix, dirsMatrix] = freqdir_spectrum(freqs, dirs, phs, ptp, pgamma, psi, pth)
% INPUT
% freqs: vector of frequencies defining output discretization (s^-1)
% dirs: vector of directions defining output discretization (degrees)
% partitions: struct with fields hsi, tpi, sii, thi being i the part number
% phs: matrix of significant wave heights (m), rows=times, cols=partitions
% ptp: matrix of peak periods (s), rows=times, cols=partitions
% pgamma: vector of gammas (adimensional)
% psi: vector of directional spreads (degrees)
% pth: vector of mean directions (degrees)
%
% OUTPUT
% Sthf: matrix of direction(rows) - frequency(cols) spectrum (m^2 * s)
% freqsMatrix: matrix of frequencies (s^-1)
% dirsMatrix: matrix of directions (degrees)
freqs = freqs(:);
dirs = dirs(:);
Sthf = zeros(numel(dirs), numel(freqs), size(phs,1));
[freqsMatrix, dirsMatrix] = meshgrid(freqs, dirs);
for itime = 1:size(phs,1)
    for ipart = 1:size(phs,2)
        hsi = phs(itime,ipart);
        tpi = ptp(itime,ipart);
        gammai = pgamma(ipart);
        sii = psi(itime,ipart);
        thi = pth(itime,ipart);
        
        Sfi = frequency_spectrum(freqs, hsi, tpi, gammai);
        
        Di = directional_distribution(dirs, sii, thi);
        
        Sthfi = repmat(Sfi(:)',numel(dirs),1) .* repmat(Di,1,numel(freqs));
        Sthfi(isnan(Sthfi)) = 0;
        Sthf(:,:,itime) = Sthf(:,:,itime) + Sthfi;
    end
end
end

