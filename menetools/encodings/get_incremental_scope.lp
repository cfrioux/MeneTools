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

% Set the seeds as compounds available at each step. 
dscope(M, 0) :- seed(M).

#program step(t).

% Set the seeds as compounds available at each step. 
dscope(M, t) :- seed(M).

% Find the compounds reachable with the previous producible compounds.
dscope(M, t) :- product(M,R), dreaction(R),
           dscope(M2, t-1): reactant(M2,R).

% Test reversibility of reaction.
dscope(M, t) :-  reactant(M,R), dreaction(R), reversible(R),
           dscope(M2, t-1): product(M2,R).

% Check if the targets are produced.
#program check(t).
:- target(F), query(t), not dscope(F, t).

#show dscope/2.