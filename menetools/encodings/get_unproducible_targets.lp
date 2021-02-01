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

% inputs from the met_net
% reaction(R).
% reactant(M,R).
% product(M,R).
% seed(M).
% target(M).


% what is producible by all reactions

dscope(M) :- seed(M).

dscope(M) :- product(M,R), dreaction(R),
           dscope(M2) : reactant(M2,R).

dscope(M) :- reactant(M,R), dreaction(R), reversible(R),
           dscope(M2) : product(M2,R).


% unproducible targets

unproducible_target(M) :- target(M), not dscope(M).

% unproducible targets

producible_target(M) :- target(M), dscope(M).

% blop(M) :- dscope(M), not seed(M).

% #show blop/1.
#show unproducible_target/1.
#show producible_target/1.
%#show dscope/1.
