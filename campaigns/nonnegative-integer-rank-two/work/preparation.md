# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus has
120 distinct legal 3-SAT formulas: 20 hand-labelled edge cases and 100 seeded
random cases, with 64 SAT and 56 UNSAT decisions, zero to six variables and
zero to ten clauses. The generator and seeds are in `generate_cases.py`;
`cases.json` stores checked outputs. Z3 4.16.0 solves exact Boolean clauses,
models are checked by direct evaluation, UNSAT is conclusive and unknown is
an error. Exhaustive assignments agreed on all 120 formulas.

The target oracle uses exact integer arithmetic. Rank exactly two is checked
by zero determinant and a nonzero 2×2 minor. In any rank-two nonnegative
integer factorization, both columns of U and both rows of V are nonzero.
For each factor entry, a positive opposite factor entry bounds it by an
entry of M, hence by `max(M)`. The oracle enumerates all U entries in that
finite range. A nonzero 2×2 minor of U then uniquely determines each column
of V by exact rational equations; only nonnegative integer solutions that
multiply back to M are accepted. Exhausting U establishes NO-SOLUTION.

Independent full enumeration of U and V agreed with the oracle on all 288
binary rank-two 3×3 matrices. A separate matrix with entries at most two,
`[[0,1,2],[1,1,1],[2,1,0]]`, has ordinary rank two but no nonnegative
integer rank-two factorization; full bounded U,V enumeration confirmed its
NO-SOLUTION status. Hand fixtures also check valid and invalid products and
reject ordinary ranks one and three.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/nonnegative-integer-rank-two/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates seeded formulas,
rechecks source labels and witnesses, then runs independent factorization
checks. The candidate runner uses separate forward and recovery subprocesses
and up to three target factorizations per source. An incorrect injected
candidate was rejected after its target was solved and recovery invalidated.
No actual reduction candidate exists. The target oracle is polynomial in
entry magnitude, so it is intended for finite small tests and makes no
polynomial bit-complexity claim. These checks do not prove hardness.
