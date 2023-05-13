""" Basic tests for the brute force solver """

from qubo_module.brute_force_solver import BruteForceSolver

def solution_str(result) :
    """ Formats the set of optimal solutions into an easy to assert against string """
    solutions_str = '|'.join(
        [''.join([str(var) for var in solution]) for solution in result.solutions]
    )
    return f'{result.best_obj:.0f}/{result.second_best_obj:.0f} {solutions_str}'

def qubo_assert(expected_result, linear, quadratic) :
    """ Asserts that the solution to the provided model is as stated. """
    result = BruteForceSolver(linear, quadratic).solve()
    assert expected_result == solution_str(result)


def test_one_variable() :
    """ Simple tests of one variable models """
    qubo_assert( "0/1 0",   {'A' : 1  }, {})
    qubo_assert("-1/0 1",   {'A' : -1 }, {})
    qubo_assert( "0/0 0|1", {'A' : 0  }, {})

def test_two_variable() :
    """ Simple tests of two variable models """
    qubo_assert( "0/1 00",   {'A':1, 'B':1}, {})
    qubo_assert("-1/0 11",   {'A':1, 'B':1}, { ('A','B') : -3 })
    qubo_assert( "0/1 00",   {'A':2, 'B':2}, { ('A','B') : -3 })

    # These test cases have non-trivial gaps
    qubo_assert("-2/-1 11",   {'A':1, 'B':-1}, { ('A','B') : -2 })
    qubo_assert( "0/1 00",     {'A':1, 'B':1}, { ('A','B') : 3 })
    qubo_assert("-5/-1 11",     {'A':-1, 'B':-1}, { ('A','B') : -3 })

def test_xor() :
    qubo_assert( "0/1 000|011|101|110", {'A':1, 'B':1, 'C':1}, {('A','B'):1, ('A','C'):1, ('B','C'):1})

if __name__ == '__main__' :
    test_one_variable()
    test_two_variable()