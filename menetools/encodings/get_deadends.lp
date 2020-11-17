% dreaction("r1").
% dreaction("r2").
% reactant("A","r1").
% product("B","r1").
% reactant("B","r2").
% product("C","r2").

deadend_np(M) :- dreaction(R), reactant(M,R), not product(M,R2):dreaction(R2).
deadend_nc(M) :- dreaction(R), product(M,R), not reactant(M,R2):dreaction(R2).

#show deadend_np/1.
#show deadend_nc/1.
