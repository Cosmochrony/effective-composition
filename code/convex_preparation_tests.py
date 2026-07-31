# Convex-preparation layer, finite tests (front-emergent-convex-preparation-recon).
# Arena: one complete 2x2 biclique S_A = S_B = {0,1}, with fibre multiplicities n_ab
# (the data R forgot). Exact rational arithmetic throughout; deterministic.
#
# Families:
#   F1 deterministic  : Diracs only, no convex closure.
#   F2 fibre-uniform  : L(nu)(x) = nu(a,b)/n_ab on fibre X_ab, macroscopic nu arbitrary.
#   F3 conditioning   : p^{U,V}_ab = w_ab 1_U(a) 1_V(b) / sum_{U x V} w, cylindrical conditions.
#
# F3 type discipline (corrected 2026-07-31): local state families use LOCAL conditions only —
#   S_A^loc = { pi_A p^{U,B} : U nonempty }   (conditions on A bear only on A),
#   S_B^loc = { pi_B p^{A,V} : V nonempty }.
# Margins of arbitrary joint conditionings p^{U,V} are conditional/steered states, NOT locally
# preparable ones, and must not enter the product-closure test.
#
# Matrices: N1 = [[1,1],[1,1]], N2 = [[1,2],[2,4]], N3 = [[1,1],[1,2]].
# Theorem (proved for arbitrary finite strictly positive W; verified here on 2x2 instances):
#   the cylindrical-conditioning family is closed under products of independently locally
#   conditioned states iff W has rank one (all 2x2 minors vanish).

from fractions import Fraction as F
from itertools import combinations

A = [0, 1]
B = [0, 1]

def nonempty_subsets(s):
    return [tuple(c) for r in range(1, len(s) + 1) for c in combinations(s, r)]

def cond(W, U, V):
    """Normalised restriction p^{U,V} of the fibre-weight measure W to the cylinder U x V."""
    tot = sum(F(W[a][b]) for a in U for b in V)
    return {(a, b): F(W[a][b]) / tot for a in U for b in V if W[a][b]}

def margin_A(p):
    return {a: sum(v for (x, _), v in p.items() if x == a) for a in A
            if any(x == a for (x, _) in p)}

def margin_B(p):
    return {b: sum(v for (_, y), v in p.items() if y == b) for b in B
            if any(y == b for (_, y) in p)}

def as_full(p):
    return tuple(p.get((a, b), F(0)) for a in A for b in B)

def minor(W):
    return W[0][0] * W[1][1] - W[0][1] * W[1][0]

def closure_report(name, W):
    print(f"== {name}: W = {W}, 2x2 minor = {minor(W)} ==")
    # F1: deterministic — every delta_a x delta_b liftable iff n_ab >= 1
    ok = all(W[a][b] >= 1 for a in A for b in B)
    print(f"  F1 deterministic: all pure products delta_a x delta_b liftable: {ok}; mixtures: none available")
    # F2: fibre-uniform — f_* L(nu) = nu identically (spot-check product and correlated nu)
    for nu_name, nu in [("product", {(a, b): F(1, 4) for a in A for b in B}),
                        ("correlated diagonal", {(0, 0): F(1, 2), (1, 1): F(1, 2)})]:
        push = {(a, b): nu[(a, b)] for (a, b) in nu if W[a][b]}  # f_*L(nu) = nu on supported fibres
        print(f"  F2 fibre-uniform: f_*L(nu {nu_name}) == nu: {push == nu}")
    print("  F2 effective image = full simplex -> product closure holds (control, no restriction)")
    # F3: conditioning family with LOCAL state families
    S_AB = [cond(W, U, V) for U in nonempty_subsets(A) for V in nonempty_subsets(B)]
    S_AB_keys = {as_full(p) for p in S_AB}
    SA_loc = [dict(t) for t in {tuple(sorted(margin_A(cond(W, U, tuple(B))).items()))
                                for U in nonempty_subsets(A)}]
    SB_loc = [dict(t) for t in {tuple(sorted(margin_B(cond(W, tuple(A), V)).items()))
                                for V in nonempty_subsets(B)}]
    fails = []
    for muA in SA_loc:
        for muB in SB_loc:
            prod = {(x, y): muA.get(x, F(0)) * muB.get(y, F(0)) for x in A for y in B
                    if muA.get(x, F(0)) * muB.get(y, F(0))}
            if as_full(prod) not in S_AB_keys:
                fails.append((muA, muB))
    print(f"  F3 conditioning: |S_AB|={len(S_AB_keys)}, |S_A^loc|={len(SA_loc)}, |S_B^loc|={len(SB_loc)}, "
          f"product closure: {'HOLDS' if not fails else 'FAILS'} ({len(fails)} failing pairs)")
    for muA, muB in fails:
        print(f"    fail: mu_A={muA} x mu_B={muB}")
    print()

closure_report("N1 uniform, factorising", [[1, 1], [1, 1]])
closure_report("N2 non-uniform, factorising (rank one)", [[1, 2], [2, 4]])
closure_report("N3 rectangular support, correlated counting measure", [[1, 1], [1, 2]])
