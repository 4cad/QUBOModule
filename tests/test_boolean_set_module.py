""" Basic tests of user defined boolean set modules. """
#pylint: disable=missing-function-docstring line-too-long
from math import isclose
import itertools
import pytest
from qubo_module.boolean_set_module import BooleanSetModule
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

def element_to_string(x) :
    return ''.join([str(char) for char in x])

def validate_set_module(set_str) :
    module = BooleanSetModule(set_str)
    embedding = module.embed()
    result = BruteForceSolver(embedding.linear, embedding.quadratic).solve()
    optimal_obj = result.best_obj

    # Each element should appear exactly once
    actual_elements = set()
    def validate_embedding(solution, obj) :
        element, _ = embedding.map_to_element(solution)
        if element is not None :
            #assert isclose(obj, optimal_obj, rel_tol=1e-6)
            element_str = element_to_string(element)
            #assert not element_str in actual_elements # Each element should be in exactly one optimal solution
            actual_elements.add(element_str)
        else :
            assert not isclose(obj, optimal_obj, rel_tol=1e-6)

    solver = BruteForceSolver(embedding.linear, embedding.quadratic)
    solver.for_each_solution(validate_embedding)

    assert actual_elements == module.element_string_set
    assert len(actual_elements) == set_str.count('|')+1

def test_embedding_one_variable_sets() :
    validate_set_module('0')
    validate_set_module('0|1')

def test_embedding_two_variable_sets() :
    validate_set_module('00')
    validate_set_module('00|11')
    validate_set_module('00|10')
    validate_set_module('00|01')
    validate_set_module('00|10|01')
    validate_set_module('00|10|11')
    validate_set_module('00|01|11')
    validate_set_module('00|01|10|11')

def allsubsets(s):
    return list(itertools.chain(*[itertools.combinations(s, ni) for ni in range(len(s)+1)]))

def test_embedding_three_variable_sets() :
    # This here is the magic of quantum computing... we have to dive into the world of powersets just to test it
    states = [''.join(x) for x in list(itertools.product('01', repeat=3))]
    for subset in allsubsets(states) :
        if len(subset) == 0 :
            continue
        subset_str='|'.join(subset)
        if '000' not in subset_str :
            continue # We don't currently only support sets that contain zero
        validate_set_module(subset_str)

@pytest.mark.skip(reason="takes super long because we are doing an exponential operaton per powerset entry of an exponential")
def test_embedding_four_variable_sets() :
    states = [''.join(x) for x in list(itertools.product('01', repeat=4))]
    for subset in allsubsets(states) :
        if len(subset) == 0 :
            continue
        subset_str='|'.join(subset)
        if '0000' not in subset_str :
            continue # We don't currently only support sets that contain zero
        validate_set_module(subset_str)

if __name__ == '__main__' :
    test_embedding_three_variable_sets()