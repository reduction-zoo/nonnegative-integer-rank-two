# 3-SAT → Nonnegative integer rank two for 3×3 matrices

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

Given a 3×3 nonnegative integer matrix with binary-encoded entries of ordinary rank exactly two, find nonnegative integer U of size 3×2 and V of size 2×3 with M=UV, or report NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question would distinguish arithmetic restrictions from real rank-two factorization in the smallest nontrivial matrix shape.

## Difficulty

Scaling can change integer feasibility, so clearing rational denominators is not a valid substitute for an integer-preserving construction.

## Literature context

The known reduction compresses an arbitrary-size rank-two matrix to 3×3; it does not reduce 3-SAT to integer factorization. The paper’s search algorithm depends on entry magnitudes, not just their binary encoding lengths. No NP-hardness proof or polynomial bit-complexity algorithm for this restricted problem was located in the checked literature. Complexity open describes this classification gap; it is not an author-stated NP-hardness conjecture.

Literature checked 2026-09-20. Checked on 2026-09-20: arXiv v2, Lemma 2.9, the construction preceding Theorem 2.10, Section 3.1, the conclusion and version history. Web searches covered the paper identifier, rank2 problem complexity, and nonnegative integer rank with NP-hardness and 3×3 restrictions. No resolving result was located. This is a bounded literature assessment, not an exhaustive novelty certificate.

## References

- [Matrices of nonnegative integer rank two](https://arxiv.org/html/2602.05957v2): Gouveia and Wiebe, arXiv:2602.05957v2. Lemma 2.9 supplies lattice-isomorphism recovery; Theorem 2.10 gives the 3×3 compression. Section 3.1 bounds the search using numerical magnitudes. The theorem’s additional magnitude bound is not justified by the described construction: take A_N with rows (N,0,N), (0,1,1), (N,1,N+1). The first two rows are primitive extreme generators of its row lattice, so the first compression retains them. Its third row has the form a(N,0,N)+b(0,1,1) for positive integers a,b. After transposition the primitive extreme rows are (N,0,aN) and (0,1,b), which the second compression retains. Thus an output entry remains N for fixed input dimensions. This direct check prevents treating that magnitude claim as a polynomial-time decision algorithm; it does not establish hardness.
- [PDF](https://arxiv.org/pdf/2602.05957v2): PDF of the same primary source; Theorem 2.10 and the runtime discussion in Section 3.1.

Fixed from board record `website/questions/nonnegative-integer-rank-two.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
