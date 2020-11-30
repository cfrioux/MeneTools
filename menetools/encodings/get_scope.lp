% scope of the seeds in the metabolic network
dscope(M) :- product(M,R), dreaction(R),
                dscope(M2) : reactant(M2,R).
    dscope(M) :- reactant(M,R), dreaction(R), reversible(R),
                dscope(M2) : product(M2,R).
    dscope(M) :- seed(M).

% activated reactions in the metabolic network
activated(R) :- dreaction(R),
            dscope(M2) : reactant(M2,R).
activated(R) :- dreaction(R), reversible(R),
            dscope(M2) : product(M2,R).

% seeds that can also be produced
produced_seed(M):- product(M,R), dreaction(R), activated(R), seed(M).
produced_seed(M):- reactant(M,R), dreaction(R), activated(R), reversible(R), seed(M).

#show dscope/1.
#show produced_seed/1.
