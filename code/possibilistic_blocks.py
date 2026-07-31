# Exhaustive possibilistic-block classification for the emergent-composition front.
# Reduction: all structure is the bipartite relation R = Pi_AB(A_0) <= O_A x O_B.
# Cylindrical conditions select S_A, S_B; combined support is sel = R & (S_A x S_B).
# Test 1 (margin stability): pi_A(sel) = S_A and pi_B(sel) = S_B
#   (extensional representatives: S_A <= pi_A(R), S_B <= pi_B(R), so pi_A(R) & S_A = S_A).
# Test 2 (joint rectangularity): sel = pi_A(sel) x pi_B(sel)  (complete biclique).
# Deterministic, no randomness, pure enumeration.

from itertools import chain, combinations

def powerset(s):
    s = sorted(s)
    return [frozenset(c) for c in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))]

def classify(name, R):
    R = frozenset(R)
    piA = frozenset(a for a, b in R)
    piB = frozenset(b for a, b in R)
    rows = []
    counts = {"total": 0, "t1": 0, "t2": 0, "both": 0, "incompat": 0, "both_nonempty": 0}
    both_nonempty = []
    for SA in powerset(piA):
        for SB in powerset(piB):
            sel = frozenset((a, b) for (a, b) in R if a in SA and b in SB)
            mA = frozenset(a for a, b in sel)
            mB = frozenset(b for a, b in sel)
            t1 = (mA == SA) and (mB == SB)
            t2 = sel == frozenset((a, b) for a in mA for b in mB)
            counts["total"] += 1
            if t1: counts["t1"] += 1
            if t2: counts["t2"] += 1
            if t1 and t2:
                counts["both"] += 1
                if sel:
                    counts["both_nonempty"] += 1
                    both_nonempty.append((sorted(SA), sorted(SB)))
            if not sel and SA and SB:
                counts["incompat"] += 1
    print(f"== {name} ==")
    print(f"  R = {sorted(R)}")
    print(f"  pairs (S_A,S_B) over extensional reps: {counts['total']}")
    print(f"  Test1 margin-stable: {counts['t1']}   Test2 rectangular: {counts['t2']}   "
          f"both: {counts['both']} (nonempty: {counts['both_nonempty']})   "
          f"incompatible (empty meet, nonempty S): {counts['incompat']}")
    print(f"  nonempty independence blocks (S_A, S_B):")
    for SA, SB in both_nonempty:
        print(f"    {SA} x {SB}")
    print()

# 1. complete relation on 2x2
classify("complete 2x2", [(a, b) for a in range(2) for b in range(2)])
# 2. diagonal on 2x2
classify("diagonal 2x2", [(0, 0), (1, 1)])
# 3. L-shape, three edges on 2x2
classify("L-shape {(0,0),(0,1),(1,0)}", [(0, 0), (0, 1), (1, 0)])
# 4. two disjoint rectangles on 4x4
classify("two disjoint 2x2 rectangles", [(a, b) for a in (0, 1) for b in (0, 1)] +
         [(a, b) for a in (2, 3) for b in (2, 3)])
# 5. incomplete bipartite cycle: 6-cycle on 3x3
classify("6-cycle on 3x3", [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 0)])
