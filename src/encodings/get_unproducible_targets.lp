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
