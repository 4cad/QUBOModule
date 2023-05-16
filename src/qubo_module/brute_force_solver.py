"""
Contains the brute force QUBO solver and its utilities.
"""
import itertools
from types import SimpleNamespace
import math

class BruteForceSolver :
    """ Solve a QUBO problem instance by brute force. """
    MAX_VARIABLES = 16

    def __init__(self, linear, quadratic):
        self.model = { 'linear' : linear, 'quadratic' : quadratic }
        self.variable_count = 0
        self.var_idx_by_name = {}
        self.var_name_by_idx = []
        self.linear_coeffs = []
        self.quadratic_coeffs = []


        for key in linear :
            variable = self.__process_var(key)
            self.linear_coeffs.append((variable, linear[key]))

        for key in quadratic :
            a, b = key
            v1 = self.__process_var(a)
            v2 = self.__process_var(b)
            self.quadratic_coeffs.append((v1, v2, quadratic[key]))

        if self.variable_count > BruteForceSolver.MAX_VARIABLES :
            raise ValueError(f'Too many variables! ${self.variable_count} variables found, '
                + f'max is ${BruteForceSolver.MAX_VARIABLES}.')

    def __process_var(self, var_name) :
        if not var_name in self.var_idx_by_name :
            self.var_idx_by_name[var_name] = self.variable_count
            self.var_name_by_idx.append(var_name)
            self.variable_count += 1
        return self.var_idx_by_name[var_name]

    # Returns the optimal solution
    def solve(self) :
        """ Returns the set of optimal solutions to the QUBO, the optimal energy, as well as 
        the gap between optimal and non-optimal solutions."""
        result = SimpleNamespace()
        result.solutions = []
        result.best_obj = 0
        result.second_best_obj = 0

        # First pass to calculate the optimal objective
        for solution in itertools.product([0,1], repeat=self.variable_count) :
            obj = self.__evaluate(solution)
            result.best_obj = min(result.best_obj, obj)
            result.second_best_obj = max(result.second_best_obj, obj) # Needed for upper bound

        # Second pass to construct the optimal solution set, and the gap
        for solution in itertools.product([0,1], repeat=self.variable_count) :
            obj = self.__evaluate(solution)
            if math.isclose(obj, result.best_obj, rel_tol=1e-6) :
                result.solutions.append(solution)
            else :
                result.second_best_obj = min(result.second_best_obj, obj)

        result.gap = result.second_best_obj - result.best_obj
        # We need to actually implement something here
        return result

    def __evaluate(self, solution) :
        energy = 0
        for var, coeff in self.linear_coeffs :
            energy += solution[var] * coeff
        
        for v1, v2, coeff in self.quadratic_coeffs :
            energy += solution[v1]*solution[v2]*coeff
        return energy
