""" Basic tests for a fully connected tile"""
#pylint: disable=missing-function-docstring line-too-long

import pytest
from qubo_module.tile import FullyConnectedTile

def test_invalid_inputs() :
    with pytest.raises(ValueError) as error :
        FullyConnectedTile(height=-1, width=1, internal_bit_count=0)
    assert str(error.value) == "Invalid height: -1"
    
    with pytest.raises(ValueError) as error :
        FullyConnectedTile(height=1, width=-1, internal_bit_count=0)
    assert str(error.value) == "Invalid width: -1"
    
    with pytest.raises(ValueError) as error :
        FullyConnectedTile(height=1, width=1, internal_bit_count=-1)
    assert str(error.value) == "Invalid internal_bit_count: -1"

def test_simple_cases() :
    tile = FullyConnectedTile(width=1, height=0, internal_bit_count=0)
    assert tile.var_count == 2
    assert tile.coefficients == [(tile.left[0], tile.right[0])]
    assert len(tile.top) == 0
    assert len(tile.bottom) == 0
    assert len(tile.internal) == 0
    
    tile = FullyConnectedTile(width=0, height=1, internal_bit_count=0)
    assert tile.var_count == 2
    assert tile.coefficients == [(tile.top[0], tile.bottom[0])]
    assert len(tile.left) == 0
    assert len(tile.right) == 0
    assert len(tile.internal) == 0
    
    tile = FullyConnectedTile(width=1, height=1, internal_bit_count=0)
    assert tile.var_count == 4
    assert tile.coefficients == [(tile.left[0], tile.right[0]), (tile.left[0], tile.top[0]), (tile.left[0], tile.bottom[0]), 
                                 (tile.right[0], tile.top[0]),(tile.right[0], tile.bottom[0]),
                                 (tile.top[0], tile.bottom[0])]
    assert len(tile.internal) == 0