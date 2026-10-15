function params = get_my_params(student_number)
%GET_MY_PARAMS AI 321 / EE 298 -- personalized exercise parameters.
%   params = get_my_params("2021-00000") returns a struct with a
%   deterministic seed and a few small parameters unique to your
%   official student number. Call this once at the top of your script
%   and use the returned fields wherever a machine exercise's
%   "Personalize this exercise" box tells you to.
%
%   Note: this MATLAB version and the companion AI321_student_seed.py
%   Python version do NOT produce identical seeds for the same student
%   number (different hash construction) -- that's fine, each is
%   internally consistent within whichever language you use for the
%   exercise; you don't need the two to match.
%
%   This also seeds MATLAB's global random number generator via rng(),
%   so any rand/randn/randi call after this line uses your personalized
%   seed automatically.

    sn = char(string(student_number));
    h = uint32(5381);
    for k = 1:length(sn)
        h = uint32(mod(double(h) * 33 + double(sn(k)), 2^32));
    end
    seed = double(h);

    rng(seed, 'twister');

    params.student_number = sn;
    params.seed = seed;
    params.offset_small = mod(seed, 30);        % e.g. a day/index offset, 0-29
    params.offset_large = mod(seed, 3000);       % e.g. a row offset into a long series
    params.subset_size = 30 + mod(seed, 21);     % e.g. 30-50, for "sample N series" tasks
    params.choice_of_8 = mod(seed, 8);           % e.g. selecting 1 of 8 provided variants
end
