function u = generate_aprbs(N, holdRange, ampRange, rngSeed)
%GENERATE_APRBS Amplitude-modulated Pseudo-Random Binary Sequence.
%   u = GENERATE_APRBS(N, holdRange, ampRange) generates an N-sample
%   APRBS signal: a piecewise-constant signal that holds a random
%   amplitude level for a random duration, then switches to a new
%   random level, repeated for the full N samples. This generalizes a
%   plain PRBS (which only switches between two fixed +-1 levels) by
%   drawing each segment's amplitude uniformly from ampRange instead.
%
%   Inputs:
%     N          - number of samples to generate
%     holdRange  - [minHold maxHold], segment length in samples; each
%                  segment's length is drawn uniformly (integer) from
%                  this range
%     ampRange   - [minAmp maxAmp], amplitude level; each segment's
%                  amplitude is drawn uniformly (continuous) from this
%                  range
%     rngSeed    - (optional) seed for reproducibility; if given, seeds
%                  MATLAB's global RNG with rng(rngSeed,'twister')
%                  before generating
%
%   Output:
%     u          - N-by-1 APRBS signal
%
%   Example -- small-amplitude APRBS (gentle excitation near a
%   nominal operating point):
%       u_small = generate_aprbs(2001, [20 150], [-0.2 0.2]);
%
%   Example -- large-amplitude APRBS (more aggressive excitation
%   across a wider range, matching the scale used to build your
%   assigned s#.mat's own APRBS column):
%       u_large = generate_aprbs(2001, [20 150], [-1.0 1.0]);
%
%   Then simulate your assigned system's response to either signal
%   (replace sys1/1 with your own assigned index):
%       s = load('sys1.mat'); sys = s.sys1;
%       dt = 0.05; t = (0:2000)'*dt;
%       y_small = lsim(sys, u_small, t);
%       y_large = lsim(sys, u_large, t);

    if nargin >= 4 && ~isempty(rngSeed)
        rng(rngSeed, 'twister');
    end

    u = zeros(N,1);
    idx = 1;
    while idx <= N
        seglen = randi(holdRange);
        amp = ampRange(1) + diff(ampRange)*rand();
        seg_end = min(idx + seglen - 1, N);
        u(idx:seg_end) = amp;
        idx = seg_end + 1;
    end
end
