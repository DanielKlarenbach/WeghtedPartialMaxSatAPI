import math

from pysat.card import CardEnc
from pysat.examples.musx import MUSX
from pysat.formula import WCNF
from pysat.solvers import Solver

from api.model_serializers import ClauseListSerializer


def validate_and_return_wcnf(data):
    serializer = ClauseListSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    wcnf = serializer.save()
    return wcnf

def generate_wcnf_formula(clauses):
    formula = WCNF()
    for clause in clauses:
        formula.append(clause.variables,clause.weight)
    return formula

def wmp1(solver_name, formula):
    hard_clauses = WCNF()
    hard_clauses.extend(formula.hard)
    mus_extractor = MUSX(formula=hard_clauses, solver=solver_name, verbosity=0)

    # check if hard clauses are satisfiable
    if mus_extractor.compute() is not None:
        mus_extractor.delete()
        return math.inf, []

    # cleanup
    mus_extractor.delete()

    cost = 0
    while True:
        # check if formula with even weights is satisfiable
        formula_with_even_weights = WCNF()
        formula_with_even_weights.extend(formula.soft, [1] * len(formula.soft))
        formula_with_even_weights.extend(formula.hard, [1] * len(formula.hard))
        mus_extractor = MUSX(formula=formula_with_even_weights, solver=solver_name, verbosity=0)

        # check if formula is satisfiable
        mus = mus_extractor.compute()

        # if formula is satisfiable, solve it
        if not mus:
            solver = Solver(solver_name)
            solver.append_formula(formula.soft)
            solver.append_formula(formula.hard)
            solver.solve()
            solution = solver.get_model()
            solver.delete()
            mus_extractor.delete()
            return cost, solution, formula.soft, formula.hard

        # make so indexes start from 0 rather than 1
        mus = [value - 1 for value in mus if value < len(formula.soft)]
        BV = []
        wmin = min([formula.wght[index] for index in mus])

        for clause_index in mus:
            new_literal = formula.nv + 1
            clause = formula.soft[clause_index]
            clause_weight = formula.wght[clause_index]
            if clause_weight != wmin:
                formula.append(clause, clause_weight - wmin)
            formula.append(clause + [new_literal], wmin)

            BV.append(new_literal)

        # deleting clauses and weights
        formula.soft = [formula.soft[index] for index in range(0, len(formula.soft)) if index not in mus]
        formula.wght = [formula.wght[index] for index in range(0, len(formula.wght)) if index not in mus]

        card = CardEnc.equals(lits=BV, bound=1)

        formula.extend(card)
        cost += wmin

        mus_extractor.delete()
