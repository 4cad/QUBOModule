""" Basic tests of user defined boolean set modules. """
#pylint: disable=missing-function-docstring line-too-long
import pytest
from qubo_module.boolean_set_module import BooleanSetModule
from qubo_module.tile import FullyConnectedTile
from qubo_module.brute_force_solver import BruteForceSolver

def test_invalid_input_wrong_type() :
    with pytest.raises(ValueError) as error :
        BooleanSetModule(123)
    assert str(error.value) == "BooleanSetModule currently does not support input type <class 'int'>"

def test_invalid_input_empty_set() :
    with pytest.raises(ValueError) as error :
        BooleanSetModule('')
    assert str(error.value) == "BooleanSetModule input set cannot be empty."

def test_invalid_input_bad_element_width() :
    with pytest.raises(ValueError) as error :
        BooleanSetModule('01|1')
    assert str(error.value) == "BooleanSetModule requires all set elements have the same number of bits. element '1' doesn't match first element '01'"

def test_invalid_input_invalid_character() :
    with pytest.raises(ValueError) as error :
        BooleanSetModule('a')
    assert str(error.value) == "BooleanSetModule element contains invalid character 'a'"

def test_one_variable_sets() :
    module = BooleanSetModule('1')
    assert module.elements == [[1]]

    module = BooleanSetModule('0')
    assert module.elements == [[0]]

    module = BooleanSetModule('0|1')
    assert module.elements == [[0], [1]]


def test_two_variable_sets() :
    # equality constraint
    module = BooleanSetModule('00|11')
    assert module.elements == [[0,0],[1,1]]

    # and constraint
    module = BooleanSetModule('11')
    assert module.elements == [[1,1]]
    
    # or constraint
    module = BooleanSetModule('01|10|11')
    assert module.elements == [[0,1],[1,0],[1,1]]
    
    # not equals constraint
    module = BooleanSetModule('01|10')
    assert module.elements == [[0,1],[1,0]]

def test_three_variable_sets() :
    # xor(a,b)
    module = BooleanSetModule('110|101|011')
    assert module.elements == [[1,1,0], [1,0,1], [0,1,1]]


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


def test_embedding_single_variable_sets() :
    module = BooleanSetModule('0')
    embedding = module.embed()
    qubo_assert("0/10 0", embedding.linear, embedding.quadratic)

if __name__ == '__main__' :
    test_embedding_single_variable_sets()