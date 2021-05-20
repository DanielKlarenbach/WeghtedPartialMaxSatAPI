# Create your tests here.

from django.test import TestCase
from pysat.formula import WCNF
from rest_framework.exceptions import ValidationError

from api.models import Clause
from api.sat_based_wmps_solver import validate_and_return_wcnf, wmp1


class ValidateAndReturnWCNFTestCase(TestCase):

    def test_validate_and_return_wcnf_with_valid_clause_list(self):
        clauses = [([1], 1), ([2], 2), ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        request_data = {'clauses': [{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses]}

        result_clauses = validate_and_return_wcnf(request_data)
        expected_clauses = [Clause(clause_data[0], clause_data[1]) for clause_data in clauses]

        self.assertEqual(len(result_clauses), len(expected_clauses))

    def test_validate_and_return_wcnf_with_empty_clause_list(self):
        request_data = {'clauses': []}

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_with_clause_with_invalid_variable_type(self):
        clause_with_invalid_variable_type = ([2.5213], 2)
        clauses = [([1], 1), clause_with_invalid_variable_type, ([3], 3), ([-1, -2], 0), ([1, -3], 0),
                   ([2, -3], 0)]
        request_data = {'clauses': [{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses]}

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_with_clause_with_invalid_weight_type(self):
        clause_with_invalid_weight_type = ([2], "dsadasdsa")
        clauses = [([1], 1), clause_with_invalid_weight_type, ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        request_data = {'clauses': [{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses]}

        self.assertRaises(ValidationError, validate_and_return_wcnf, clauses)

    def test_validate_and_return_wcnf_with_clause_with_empty_variable_list(self):
        clause_with_empty_variable_list = ([], 2)
        clauses = [([1], 1), clause_with_empty_variable_list, ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        request_data = {'clauses': [{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses]}

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_clause_with_no_weight(self):
        clause_with_no_weight = ([3])
        clauses = [([1], 1), ([2], 2), clause_with_no_weight, ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        request_data = {
            'clauses': [{'variables': clause_data[0], 'weight': None if len(clause_data) == 1 else clause_data[1]} for
                        clause_data in clauses]}

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

class WMP1TestCase(TestCase):

    def test_wmp1(self):
        formula = WCNF()
        formula.append([1], weight=1)
        formula.append([2], weight=1)
        formula.append([3], weight=1)
        formula.append([4], weight=1)
        formula.append([5], weight=1)
        formula.append([-1, -2])
        formula.append([-2, -3])
        formula.append([-3, -4])
        formula.append([-4, -5])

        result_cost, result_solution, result_final_soft_clauses, result_final_hard_clauses = wmp1(solver_name='glucose4', formula=formula)
        expected_cost = 2
        expected_solution = [1, -2, 3, -4, 5, -6, 7, -8, 9]
        expected_final_soft_clauses = [[5], [1, 6], [2, 7], [3, 8], [4, 9]]
        expected_final_hard_clauses = [[-1, -2], [-2, -3], [-3, -4], [-4, -5], [6, 7], [-6, -7], [8, 9], [-8, -9]]

        self.assertEqual(result_cost,expected_cost)
        self.assertListEqual(result_solution,expected_solution)
        self.assertListEqual(result_final_soft_clauses,expected_final_soft_clauses)
        self.assertListEqual(result_final_hard_clauses,expected_final_hard_clauses)



