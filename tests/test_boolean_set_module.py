""" Basic tests of user defined boolean set modules. """
#pylint: disable=missing-function-docstring line-too-long
import pytest
from qubo_module.boolean_set_module import BooleanSetModule

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



if __name__ == '__main__' :
    test_invalid_input_empty_set()