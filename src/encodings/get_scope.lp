dscope(M) :- product(M,R), dreaction(R),
                dscope(M2) : reactant(M2,R).
    dscope(M) :- reactant(M,R), dreaction(R), reversible(R),
                dscope(M2) : product(M2,R).
    dscope(M) :- seed(M).

#show dscope/1.
