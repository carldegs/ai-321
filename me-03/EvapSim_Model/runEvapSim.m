function p = runEvapSim(show,amp,L)
%   runEvapSim.m runs the Evaporator Sim,
%   giving p as the datasets. 
%
%   Author: Karl Ezra S. Pilario
%
%   Input: show = 1,   if you want to plot results
%                 0,   if no plot is desired
%          amp  = 1,   if you want small input amplitudes
%                 2,   if you want large input amplitudes
%                 1:2, if you want both small and large
%          L    = number of samples (default: 1001)
%
%   Output:  p = data set, size: [L x 6]
%   Columns: F200, P100, F3, L2, P2, X2
%
%   Try these examples:
%   >> p = runEvapSim(1);
%   >> p = runEvapSim(1,1);
%   >> p = runEvapSim(1,2);
%   >> p = runEvapSim(1,1:2);

    %% Generate Training and Test Data Sets
    if nargin < 3, L = 6001; end
    if nargin < 2, amp = 1; end
    if nargin < 1, show = 1; end
    
    p = cell(length(amp),1); close all;
    in = Simulink.SimulationInput('evapSimNew');

    t = (0:0.5:3000)'; N = length(t);
    u = zeros(N,8);
    % Inputs: [L2sp F200 P100 T200 F1 X1 T1 F3];
    a =       [0    120  120  0    0  0  0  5;...
               0    150  150  0    0  0  0  6.25]; % Input amplitudes
    
    C = 25; H = ceil(L/C);                  % C = no. of input changes
    for j = 1:length(amp)
        for m = 1:8
            ut = zeros(C,1);
            % Amplitude-modulated PRBS
            for k = 1:C
                ut(k) = a(amp(j),m)*(rand - 0.5)*2;
            end
            vt = repmat(ut,1,H)';
            vt = [zeros(H+1,1); vt(:)];
            u(:,m) = vt(1:N);
        end

        in.ExternalInput = [t, u]; out = sim(in);
        InpNom = [1 208 194.7 25 10 5 40 50];
        
        inps = [2:3 8];     % Input variable indices
        p{j} = [u(:,inps)+repmat(InpNom(inps),N,1) out.States];
        p{j} = p{j}(1:L,:);
        
        s = [5 5 0.5 0.05 1 2]; % noise variance vector
                                % [F200 P100 F3 L2 P2 X2]
        for m = 1:length(s)
            p{j}(:,m) = p{j}(:,m) + (rand(L,1) - 0.5)*s(m);
        end
    end
    if show
        if length(amp) == 1
            visEvap(p{1},[],t(1:L));
        else
            visEvap(p{1},p{2},t(1:L)); 
        end
    end
end