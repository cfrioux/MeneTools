% Copyright (C) Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU Lesser General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU Lesser General Public License for more details.
% You should have received a copy of the GNU Lesser General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>

#include <incmode>.

#program base.

% Set the seeds as compounds producible at step 0.
dscope(M, 0) :- seed(M).

#program step(t).

% Set the seeds as compounds producible at each step.
dscope(M, t) :- seed(M).

% Find the compounds producible from the producible compounds of the previous step (plus the seeds).
dscope(M, t) :- product(M,R), dreaction(R),
           dscope(M2, t-1): reactant(M2,R).

% Test reversibility of reaction.
dscope(M, t) :-  reactant(M,R), dreaction(R), reversible(R),
           dscope(M2, t-1): product(M2,R).

% Compute the size of the scope at each step t.
dscopeSize(ScopeSize, t) :- ScopeSize=#sum{1,M : dscope(M, t)}.

% Two possible goals:
% - either targets are given as input and the programm will check the number of step to produce these targets. WARNING if the targets are not producible, it will enter an infinite loop.
% - or it will try to reach the same scope size as the one computed from a menescope (by using maxscope(MaxScope) given as input).
#program check(t).
:- target(F), query(t), not dscope(F, t).
:- not dscopeSize(ScopeSize, t), query(t), maxscope(MaxScope), ScopeSize == MaxScope.

#show dscope/2.
