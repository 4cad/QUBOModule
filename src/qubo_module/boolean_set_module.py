"""
The boolean set module is a convenience wrapper for QUBO modules that enforce a beeloan set 
constraint by ensuring a module solution is optimal if and only if the external variable values
are in the user provided set."""

class BooleanSetModule :
    """ Wraps a set of boolean vectors. Can be embedded onto a tile."""
    def __init__(self, set) :
        if isinstance(set, str) :
            elements = set.split('|')
            if len(elements) == 0 or len(elements[0]) == 0:
                raise ValueError("BooleanSetModule input set cannot be empty.")

            width = len(elements[0])
            for element in elements :
                if width != len(element) :
                    raise ValueError(
                        "BooleanSetModule requires all set elements have the same number of bits. "+
                        f"element '{element}' doesn't match first element '{elements[0]}'")
        else :
            raise ValueError(f'BooleanSetModule currently does not support input type {type(set)}')
