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

% dreaction("r1").
% dreaction("r2").
% reversible("r1").
% reactant("A","r1").
% product("B","r2").
% reaction("r3").
% reactant("C").

% The above example identifies A and B as seeds.

seed(M) :- reactant(M,R) ; not product(_, R) ; reversible(R) ; dreaction(R).
seed(M) :- product(M,R) ; not reactant(_,R) ; dreaction(R).

#show seed/1.

