/* ------------------------------------------------------------------------
   A very simple grammar
   Definite-clause grammar notation.
   Augmented to encapsulate the lexical rules.
   Incorporates subject-verb number and person agreement.
   Builds parse trees.

   Stuart Shieber
   CS187

   $Id: frog-toad-3a.pl,v 1.1 2005/10/03 20:16:15 shieber Exp $
   ------------------------------------------------------------------------ */

%%% The grammar

s(Agr, s(NP, VP)) --> np(Agr, NP), vp(Agr, VP,_,_).

%% Prepositional phrases

s(Agr, s(NP, VP, Prep)) --> np(Agr, NP), vp(Agr, VP,_,_), pp(Prep).

%% Verbal phrases

vp(Agr, vp(V), intransitive, Conj) --> v(Agr, V, intransitive, Conj).
vp(Agr, vp(V, Comps), Type, Conj) --> v(Agr, V, Type,Conj), cp(Type, Comps).

%% Auxiliar verbs

vp(Agr, vp(Aux, V), intransitive, Conj) --> aux(Aux, Conj / Req), vp(Agr, V, intransitive, Req).
vp(Agr, vp(Aux, Rest), Type, Conj) --> aux(Aux, Conj / Req), vp(Agr, Rest, Type, Req).

%% Verbal complements

cp(transitive, cp(NP)) --> np(_, NP).
cp(ditransitive, cp(NP1, NP2)) --> np(_, NP1), np(_, NP2).
cp(dative(Prep), cp(NP1, pp(pp(p(Prep), NP2)))) --> np(_, NP1), pp(pp(p(Prep), NP2)).

%% Prepositional phrases

pp(pp(Prep, NP)) --> p(Prep), np(_, NP).
np(Agr, np(Det, N, Prep)) --> det(Agr, Det), n(Agr, N), pp(Prep).

%% Possessive

%% basic rules for NP
np(Agr, np(PN)) --> pn(Agr, PN).
np(Agr, np(Det, N)) --> det(Agr, Det), n(Agr, N).

%% NP with possessive (should agree with last element)
np(Agr, np(PN, Rest)) --> pn(_, PN), np_prime(Agr, Rest).
np(Agr, np(Det, N, Rest)) --> det(A, Det), n(A, N), np_prime(Agr, Rest).

%% possessive rules
np_prime(Agr, np([s], N, Rest)) --> [s], n(_, N), np_prime(Agr, Rest).
np_prime(Agr, np([s], N)) --> [s], n(Agr, N).

%%% The lexicon

%% Proper nouns

pn(agr(sg,third), pn(X)) --> [X], {pn(X)}.

pn(frog).
pn(toad).

%% Verbs

v(agr(sg,first), v(X), Type, Conj) --> [X], {vlex(X,_,_,_,Type,Conj)}.
v(agr(sg,second), v(X), Type, Conj) --> [X], {vlex(_,X,_,_,Type,Conj)}.
v(agr(sg,third), v(X), Type, Conj) --> [X], {vlex(_,_,X,_,Type,Conj)}.
v(agr(pl,_), v(X), Type, Conj) --> [X], {vlex(_,_,_,X,Type,Conj)}.

% to meet

vlex(meet, meet, meets, meet, transitive, finite).
vlex(meeting, meeting, meeting, meeting, transitive, present).
vlex(met, met, met, met, transitive, past).
vlex(meet, meet, meet, meet, transitive, nonfinite).

% to be

vlex(am, are, is, are, transitive, finite).
vlex(being, being, being, being, transitive, present).
vlex(been, been, been, been, transitive, past).
vlex(be, be, be, be, transitive, nonfinite).

% to bake

vlex(bake, bake, bakes, bake, ditransitive, finite).
vlex(bake, bake, bakes, bake, transitive, finite).
vlex(bake, bake, bakes, bake, dative(for), finite).
vlex(bake, bake, bakes, bake, dative(in), finite).

vlex(baking, baking, baking, baking, ditransitive, present).
vlex(baking, baking, baking, baking, transitive, present).
vlex(baking, baking, baking, baking, dative(for), present).
vlex(baking, baking, baking, baking, dative(in), present).

vlex(baked, baked, baked, baked, ditransitive, past).
vlex(baked, baked, baked, baked, transitive, past).
vlex(baked, baked, baked, baked, dative(for), past).
vlex(baked, baked, baked, baked, dative(in), past).

vlex(bake, bake, bake, bake, ditransitive, nonfinite).
vlex(bake, bake, bake, bake, transitive, nonfinite).
vlex(bake, bake, bake, bake, dative(for), nonfinite).
vlex(bake, bake, bake, bake, dative(in), nonfinite).

% to put

vlex(put, put, puts, put, dative(in), finite).
vlex(putting, putting, putting, putting, dative(in), present).
vlex(put, put, put, put, dative(in), past).
vlex(put, put, put, put, dative(in), nonfinite).

% to die

vlex(die, die, dies, die, intransitive, finite).
vlex(dying, dying, dying, dying, intransitive, present).
vlex(died, died, died, died, intransitive, past).
vlex(die, die, die, die, intransitive, nonfinite).

% to give

vlex(give, give, gives, give, ditransitive, finite).
vlex(giving, giving, giving, giving, ditransitive, present).
vlex(gave, gave, gave, gave, ditransitive, past).
vlex(give, give, give, give, ditransitive, nonfinite).

vlex(give, give, gives, give, dative(to), finite).
vlex(giving, giving, giving, giving, dative(to), present).
vlex(gave, gave, gave, gave, dative(to), past).
vlex(give, give, give, give, dative(to), nonfinite).

%% Determiners

det(Agr, det(X)) --> [X], {det(X, Agr)}.

det(the,   agr(_,third)).
det(a,	   agr(sg,third)).
det(some,  agr(_,third)).
det(every, agr(sg,third)).
det(most,  agr(pl,third)).

%% Singular nouns

n(agr(sg,third), n(X)) --> [X], {n(X,_)}.
n(agr(pl,third), n(X)) --> [X], {n(_,X)}.

n(amphibian, amphibians).
n(cake,      cakes).
n(cookie,    cookies).
n(box,		 boxes).
n(cake,		 cakes).
n(kitchen, 	 kitchens).

%% Prepositions
p(p(X)) --> [X], {p(X)}.

p(for).
p(to).
p(in).
p(on).
p(above).
p(below).
p(with).
p(every).

%% Auxiliar Verbs
aux(aux(X), Form) --> [X], {aux(X,Form)}.

% can
aux(can, none / nonfinite).

% could
aux(could, finite / nonfinite).

% have
aux(have, nonfinite / past).

% been
aux(been, past / present).

% be
aux(be, nonfinite / present).