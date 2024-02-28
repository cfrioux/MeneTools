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

% filter seeds by removing those that never occur in the metabolic network
true_seed(M) :- seed(M), reactant(M, _).
true_seed(M) :- seed(M), product(M, _).

absent_seed(M) :- seed(M), not true_seed(M).

% scope of the seeds in the metabolic network
dscope(M) :- product(M,R), dreaction(R),
                dscope(M2) : reactant(M2,R).
    dscope(M) :- reactant(M,R), dreaction(R), reversible(R),
                dscope(M2) : product(M2,R).
    dscope(M) :- true_seed(M).

% activated reactions in the metabolic network
activated(R) :- dreaction(R),
            dscope(M2) : reactant(M2,R).
activated(R) :- dreaction(R), reversible(R),
            dscope(M2) : product(M2,R).

% seeds that can also be produced
produced_seed(M):- product(M,R), dreaction(R), activated(R), true_seed(M).
produced_seed(M):- reactant(M,R), dreaction(R), activated(R), reversible(R), true_seed(M).

non_produced_seed(M):- true_seed(M), not produced_seed(M).


#show dscope/1.
#show produced_seed/1.
#show non_produced_seed/1.
#show absent_seed/1.
#show activated/1.
