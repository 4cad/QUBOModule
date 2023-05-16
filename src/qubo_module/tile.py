"""
This module is for tiles, which can be created to represent features of a given QPU topology.
In the future, the intention is to split a QPU into "tiles" that allow for us to optimize the
embedding of unary functions in modular fields.
"""
import itertools

class FullyConnectedTile :
    """ Represents a fully connected tile. All qubits are connected to eachother"""
    def __init__(self, width: int, height: int, internal_bit_count: int) :
        if width < 0 :
            raise ValueError(f"Invalid width: {width}")
        if height < 0 :
            raise ValueError(f"Invalid height: {height}")
        if internal_bit_count < 0 :
            raise ValueError(f"Invalid internal_bit_count: {internal_bit_count}")
        
        self.width = width
        self.height = height
        self.internal_bit_count = internal_bit_count
        
        self.left = []
        self.right = []
        self.top = []
        self.bottom = []
        self.internal = []

        self.var_count = 0

        for _ in range(width) :
            self.left.append(self.__new_var())
            self.right.append(self.__new_var())

        for _ in range(height) :
            self.top.append(self.__new_var())
            self.bottom.append(self.__new_var())
        
        for _ in range(internal_bit_count) :
            self.internal.append(self.__new_var())

        # Since this is a fully connected tile, we are going to add a coefficient for every variable pair
        self.coefficients = []
        for a, b in itertools.product(range(self.var_count), repeat=2) :
            if a < b :
                self.coefficients.append( (a,b) )

    def __new_var(self) :
        result =  self.var_count
        self.var_count += 1
        return result

    
    