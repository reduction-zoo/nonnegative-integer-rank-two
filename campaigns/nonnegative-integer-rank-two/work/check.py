"""Independent 3-SAT and exact integer-factorization oracles."""

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def determinant(matrix):
    a, b, c = matrix
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def rank_two(matrix):
    if determinant(matrix) != 0:
        return False
    return any(matrix[i][j]*matrix[k][l] != matrix[i][l]*matrix[k][j]
               for i in range(3) for k in range(i+1, 3)
               for j in range(3) for l in range(j+1, 3))


def legal_target(target):
    if not isinstance(target, dict):
        return False
    matrix = target.get("matrix")
    return (isinstance(matrix, list) and len(matrix) == 3
            and all(isinstance(row, list) and len(row) == 3
                    and all(type(value) is int and value >= 0 for value in row)
                    for row in matrix)
            and rank_two(matrix))


def direct_factorization(target, output):
    if not legal_target(target) or not isinstance(output, dict) or set(output) != {"U", "V"}:
        return False
    U, V = output["U"], output["V"]
    if not (isinstance(U, list) and len(U) == 3 and isinstance(V, list) and len(V) == 2
            and all(isinstance(row, list) and len(row) == 2 and
                    all(type(value) is int and value >= 0 for value in row) for row in U)
            and all(isinstance(row, list) and len(row) == 3 and
                    all(type(value) is int and value >= 0 for value in row) for row in V)):
        return False
    return all(U[i][0]*V[0][j] + U[i][1]*V[1][j] == target["matrix"][i][j]
               for i in range(3) for j in range(3))


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal rank-two nonnegative integer matrix")
    M = target["matrix"]
    maximum = max(map(max, M))
    outputs = []
    for entries in product(range(maximum+1), repeat=6):
        U = [list(entries[2*i:2*i+2]) for i in range(3)]
        pivot = next(((i, k, U[i][0]*U[k][1]-U[i][1]*U[k][0])
                      for i in range(3) for k in range(i+1, 3)
                      if U[i][0]*U[k][1] != U[i][1]*U[k][0]), None)
        if pivot is None:
            continue
        i, k, det = pivot
        V = [[], []]
        for j in range(3):
            first = Fraction(M[i][j]*U[k][1]-M[k][j]*U[i][1], det)
            second = Fraction(U[i][0]*M[k][j]-U[k][0]*M[i][j], det)
            if first.denominator != 1 or second.denominator != 1 or first < 0 or second < 0:
                break
            V[0].append(int(first))
            V[1].append(int(second))
        if len(V[0]) != 3:
            continue
        output = {"U": U, "V": V}
        if direct_factorization(target, output):
            outputs.append(output)
            if len(outputs) >= limit:
                break
    return outputs or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, 1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    return direct_factorization(target, output)


def exhaustive_binary_target(target):
    for U_values in product((0,1), repeat=6):
        U = [list(U_values[2*i:2*i+2]) for i in range(3)]
        for V_values in product((0,1), repeat=6):
            V = [list(V_values[3*i:3*i+3]) for i in range(2)]
            output = {"U": U, "V": V}
            if direct_factorization(target, output):
                return output
    return {"status": "NO-SOLUTION"}


def exhaustive_small_target(target):
    maximum = max(map(max, target["matrix"]))
    for U in product(range(maximum+1), repeat=6):
        for V in product(range(maximum+1), repeat=6):
            if all(U[2*i]*V[j] + U[2*i+1]*V[3+j] == target["matrix"][i][j]
                   for i in range(3) for j in range(3)):
                return True
    return False


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(path)], check=True, cwd=root)
    cases = json.loads(path.read_text())
    for n, clauses, answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars": n, "clauses": clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                         for clause in source["clauses"])
                     for bits in product((False, True), repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source, current) and valid_source(source, case["expected"])
    test_hand_cases()
    checked = 0
    for entries in product((0,1), repeat=9):
        target = {"matrix": [list(entries[3*i:3*i+3]) for i in range(3)]}
        if legal_target(target):
            assert ("U" in solve_target(target)) == ("U" in exhaustive_binary_target(target))
            checked += 1
    assert not exhaustive_small_target({"matrix": [[0,1,2],[1,1,1],[2,1,0]]})
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} binary rank-two matrices")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target matrix: {target}")
        for output in target_solutions(target):
            if not valid_target(target, output):
                raise AssertionError(f"Target oracle returned invalid output: {output}")
            payload = {"source": source, "target_solution": output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source, recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
