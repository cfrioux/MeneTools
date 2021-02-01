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

activ(R) :- dreaction(R),
            dscope(M2) : reactant(M2,R).
activ(R) :- dreaction(R), reversible(R),
            dscope(M2) : product(M2,R).

#show activ/1.
