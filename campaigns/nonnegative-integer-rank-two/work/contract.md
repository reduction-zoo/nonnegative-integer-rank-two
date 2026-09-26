# Prepared input and output contract

The 3-SAT source input is `{"num_vars": n, "clauses": [[signed_literals],
...]}` with `n >= 0`, at most three literals per clause and each nonzero
literal's absolute value at most `n`. A source output is
`{"assignment": [bool, ...]}` satisfying all clauses, or
`{"status": "NO-SOLUTION"}` exactly when none exists.

The target input is `{"matrix": [[nonnegative_integer, ...], ...]}` with
exactly three rows of three entries and ordinary matrix rank exactly two.
An output is `{"U": [[...], [...], [...]], "V": [[...], [...]]}` with
nonnegative integer `U` of shape 3×2 and `V` of shape 2×3 such that `UV=M`.
`{"status": "NO-SOLUTION"}` is valid exactly when no such factors exist.
All entries are exact binary-encoded integers; no rational factorization is
accepted.

A candidate `algorithm.py` reads a source JSON object from stdin and writes
a legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors, and send
diagnostics to stderr. They must be deterministic and polynomial time, and
recovery must work for every valid integer factorization or NO-SOLUTION.

`check.py --candidate PATH` independently solves each constructed target on
the fixed source corpus and directly validates each recovered source output.
