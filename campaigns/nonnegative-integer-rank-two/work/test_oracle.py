from check import legal_target, solve_target, valid_target


def test_hand_cases():
    diag = {"matrix": [[1,0,0],[0,1,0],[0,0,0]]}
    assert legal_target(diag)
    assert valid_target(diag, {"U": [[1,0],[0,1],[0,0]], "V": [[1,0,0],[0,1,0]]})
    assert not valid_target(diag, {"U": [[0,0]]*3, "V": [[0,0,0]]*2})
    assert "U" in solve_target(diag)
    assert not legal_target({"matrix": [[1,0,0],[0,0,0],[0,0,0]]})
    assert not legal_target({"matrix": [[1,0,0],[0,1,0],[0,0,1]]})
    no_integer_factorization = {"matrix": [[0,1,2],[1,1,1],[2,1,0]]}
    assert legal_target(no_integer_factorization)
    assert solve_target(no_integer_factorization) == {"status": "NO-SOLUTION"}


if __name__ == "__main__":
    test_hand_cases()
