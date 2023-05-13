"""
The boolean set module is a convenience wrapper for QUBO modules that enforce a beeloan set 
constraint by ensuring a module solution is optimal if and only if the external variable values
are in the user provided set."""

class BooleanSetModule :
    """ Wraps a set of boolean vectors. Can be embedded onto a tile."""
    def __init__(self, input_set) :
        self.elements = []
        if isinstance(input_set, str) :
            elements = input_set.split('|')
            if len(elements) == 0 or len(elements[0]) == 0:
                raise ValueError("BooleanSetModule input set cannot be empty.")

            self.width = len(elements[0])
            for element in elements :
                if self.width != len(element) :
                    raise ValueError(
                        "BooleanSetModule requires all set elements have the same number of bits. "+
                        f"element '{element}' doesn't match first element '{elements[0]}'")
                self.__add_string_element(element)

        else :
            raise ValueError(f'BooleanSetModule currently does not support input type {type(input_set)}')

    def __add_string_element(self, element) :
        new_element = []
        for bit in element :
            if bit == '0' :
                new_element.append(0)
            elif bit == '1' :
                new_element.append(1)
            else :
                raise ValueError(f"BooleanSetModule element contains invalid character '{bit}'")
        self.elements.append(new_element)