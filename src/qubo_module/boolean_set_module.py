"""
The boolean set module is a convenience wrapper for QUBO modules that enforce a beeloan set 
constraint by ensuring a module solution is optimal if and only if the external variable values
are in the user provided set."""

from types import SimpleNamespace

from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit

from .tile import FullyConnectedTile

LP_VAR_LOWER=-100
LP_VAR_UPPER=100

class BooleanSetModule :
    """ Wraps a set of boolean vectors. Can be embedded onto a tile."""

    def __init__(self, input_set) :
        self.elements = []
        self.element_set = set()
        self.enable_experimental_mip_embedding = False
        self.has_zero = False
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
        
        element_as_int = int(element, 2)
        if element_as_int is 0 :
            self.has_zero = True
        self.element_set.add(element_as_int)
        self.elements.append(new_element)
    
    def embed(self) :
        """ Simple inefficient embedding, with one qubit per set element """
        model = SimpleNamespace()
        model.linear = dict()
        model.quadratic = dict()
        
        # One variable for each of the external bits in the set. If 0 is in the set, we have to do things differently
        if self.has_zero :
            BASE_PENALTY = 10
            # Lets start by punishing any bits for being 1
            for i in range(self.width) :
                model.linear[f'bit_{i}'] = BASE_PENALTY
            
            # Now we add a var for every element
            for x in self.elements :
                ones_count = 0
                zeros_count = 0
                for i in range(self.width) :
                    if x[i] == 0 :
                        zeros_count += 1
                    else :
                        ones_count += 1
                
                if ones_count == 0 :
                    continue # We already designed this one in, it is the zero element
                
                # So we have bit_count * 10 penalty from the linear constraints, which we have to undo with the quadratic constraints on the 1 elements
                weight = ones_count * BASE_PENALTY / self.width

                for i in range(self.width) :
                    if x[i] == 0 :
                        coeff = -weight
                    else :
                        coeff = weight
                    model.quadratic[(f'bit_{i}', f'indicator_{str(x)}')] = coeff
        else :
            raise NotImplementedError('Do not currently support bit sets that have no zero element.')

        return model
        
    
    def embed_onto_tile_mip(self, tile : FullyConnectedTile) :
        """ Embeds this boolean set onto the tile, raising an exception if it does not fit on the tile """
        
        if not self.enable_experimental_mip_embedding :
            raise NotImplementedError("Implementing this MIP based embedding been deferred until we have a working end-to-end case")
    
        pywrapinit.CppBridge.InitLogging('basic_example.py')
        cpp_flags = pywrapinit.CppFlags()
        cpp_flags.logtostderr = True
        cpp_flags.log_prefix = False
        pywrapinit.CppBridge.SetFlags(cpp_flags)

        solver = pywraplp.Solver.CreateSolver('CLP')
        if not solver:
            raise RuntimeError('BooleanSetModule was unable to instantiate an instance of CLP solver through ortools.')
        
        infinity = solver.infinity()
        objective = solver.Objective()
        lp_vars = []
        for i in range(tile.var_count) :
            v = solver.NumVar(LP_VAR_LOWER, LP_VAR_UPPER, f'linear_{i}')
            lp_vars.append( (v, i, i) )

        for i, j in tile.coefficients :
            v = solver.NumVar(LP_VAR_LOWER, LP_VAR_UPPER, f'quadratic_{i}_{j}')
            lp_vars.append( (v, i, j) )

        gap_var = solver.NumVar(0, LP_VAR_UPPER, 'gap')
        objective.SetCoefficient(gap_var, 100) # Maximize the gap!
        objective.SetMaximization()

        print('Number of variables =', solver.NumVariables())

        solution = [0 for i in range(self.width)]
        for solution_int in range(2**self.width) :
            if solution_int in self.element_set :
                # The RHS here should be 0
                constraint = solver.Constraint(0, 0, f'constraint_{i}_pass')
            else :
                constraint = solver.Constraint(0, infinity, f'constraint_{i}_reject')
                constraint.SetCoefficient(gap_var, -1) #
            
            bit = 1
            for i in range(self.width) :
                if (solution_int & bit) == 0 :
                    solution[i] = 0
                else :
                    solution[i] = 1
                bit = bit << 1

            for var, i, j in lp_vars :
                if solution[i]*solution[j] == 1:
                    # This term is active! So lets add it to the constraint
                    constraint.SetCoefficient(var, 1)
    
        solver.Solve()

        print('Solution:')
        print('  Objective value =', objective.Value())
        print(f'  gap={gap_var.solution_value()}')
        
        for var, i, j in lp_vars :
            print(f'{var.Name()} = {var.solution_value()} - term ({i}, {j})')

        return {}
