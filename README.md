# 3-SAT → Nonnegative integer rank two for 3×3 matrices

Independent research campaign for the [fixed question](campaigns/nonnegative-integer-rank-two/question.md). [State](campaigns/nonnegative-integer-rank-two/state.md) records the current evidence and next action.

The initial commit fixes the question and setup. [Prepare evidence](campaigns/nonnegative-integer-rank-two/work/preparation.md), [contract](campaigns/nonnegative-integer-rank-two/work/contract.md), and [fixed corpus](campaigns/nonnegative-integer-rank-two/work/cases.json) are committed. No solution is claimed. Run the campaign from this repository and follow `AGENTS.md`.

Reproduce: `uv sync --locked`, then `uv run --locked python campaigns/nonnegative-integer-rank-two/work/check.py --self-test`.
