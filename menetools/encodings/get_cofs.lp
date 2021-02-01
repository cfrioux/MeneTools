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

    dscope(M) :- product(M,R), dreaction(R),
                dscope(M2) : reactant(M2,R).
    dscope(M) :- reactant(M,R), dreaction(R), reversible(R),
                dscope(M2) : product(M2,R).
    dscope(M) :- seed(M).

    allscope(M) :- product(M,R), dreaction(R),
                allscope(M2) : reactant(M2,R).
    allscope(M) :- reactant(M,R), dreaction(R), reversible(R),
                allscope(M2) : product(M2,R).
    allscope(M) :- seed(M).
    allscope(M) :- cofactor(M).

    {needed_cof(M) : cofactor(M)}.

    xscope(M) :- product(M,R), dreaction(R),
                xscope(M2) : reactant(M2,R).
    xscope(M) :- reactant(M,R), dreaction(R), reversible(R),
                xscope(M2) : product(M2,R).
    xscope(M) :- seed(M).
    xscope(M) :- needed_cof(M).


    :- target(M), allscope(M), not xscope(M).

    still_unprod(M) :- target(M), not allscope(M).

    newly_prod(M) :- target(M), xscope(M), not dscope(M).

    %minimize the number of cofactors which are actually targets
        #minimize { 1@3, M : needed_cof(M), target(M)}.
    %minimize the number of unproducible targets
        #minimize { 1@2,M : still_unprod(M) ; 0@3}.
    %minimize the number of cofcators
        #minimize { 1@1,R : needed_cof(R)}.


#show still_unprod/1.
#show needed_cof/1.
#show newly_prod/1.
