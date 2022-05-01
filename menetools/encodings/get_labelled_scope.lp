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

product_r(M,R,Nb) :- dscope(M,Nb), product(M,R).
reactant_r(M,R,Nb) :- dscope(M,Nb), reactant(M,R).

% scope of the seeds in the metabolic network
dscope(M,Nb) :- product(M,R), dreaction(R), reactant_r(M2,R,Nb),
                dscope(M2,Nb) : reactant(M2,R).
dscope(M,Nb) :- reactant(M,R), dreaction(R), reversible(R), product_r(M2,R,Nb),
            dscope(M2,Nb) : product(M2,R).
dscope(M,Nb) :- seed(M,Nb).

% activated reactions in the metabolic network
activated(R) :- dreaction(R), reactant_r(M2,R,Nb),
            dscope(M2,Nb) : reactant(M2,R).
activated(R) :- dreaction(R), reversible(R), product_r(M2,R,Nb),
            dscope(M2,Nb) : product(M2,R).

% seeds that can also be produced
produced_seed(M):- product(M,R), dreaction(R), activated(R), seed(M,Nb).
produced_seed(M):- reactant(M,R), dreaction(R), activated(R), reversible(R), seed(M,Nb).

#show dscope/2.
#show produced_seed/1.
