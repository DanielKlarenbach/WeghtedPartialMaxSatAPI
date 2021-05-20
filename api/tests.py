# Create your tests here.
import json

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer

from api.models import Clause
from api.sat_based_wmps_solver import validate_and_return_wcnf


class ValidateAndReturnWCNFTestCase(TestCase):

    def test_validate_and_return_wcnf_with_valid_clause_list(self):
        clauses_data = [([1], 1), ([2], 2), ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        clauses ={'clauses' : [{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses_data]}
        request_data =  JSONRenderer().render(clauses)

        result_clauses = validate_and_return_wcnf(request_data)
        expected_clauses = [Clause(clause_data[0],clause_data[1]) for clause_data in clauses_data]

        self.assertListEqual(result_clauses, expected_clauses)

    def test_validate_and_return_wcnf_with_empty_clause_list(self):
        clauses ={'clauses' : []}
        request_data =  JSONRenderer().render(clauses)

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_with_clause_with_invalid_variable_type(self):
        clause_with_invalid_variable_type = ([2.5213], 2)
        clauses_data = [([1], 1), clause_with_invalid_variable_type, ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        clauses = {'clauses' : [{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses_data]}
        request_data =  JSONRenderer().render(clauses)

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_with_clause_with_invalid_weight_type(self):
        clause_with_invalid_weight_type = ([2], "dsadasdsa")
        clauses_data = [([1], 1), clause_with_invalid_weight_type, ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        clauses = {'clauses' :[{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses_data]}
        request_data =  JSONRenderer().render(clauses)

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_with_clause_with_empty_variable_list(self):
        clause_with_empty_variable_list = ([], 2)
        clauses_data = [([1], 1), clause_with_empty_variable_list , ([3], 3), ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        clauses = {'clauses' :[{'variables': clause_data[0], 'weight': clause_data[1]} for clause_data in clauses_data]}
        request_data =  JSONRenderer().render(clauses)

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)

    def test_validate_and_return_wcnf_clause_with_no_weight(self):
        clause_with_no_weight = ([3])
        clauses_data = [([1], 1), ([2], 2),clause_with_no_weight, ([-1, -2], 0), ([1, -3], 0), ([2, -3], 0)]
        clauses = {'clauses' :[{'variables': clause_data[0], 'weight': None if len(clause_data)==1 else clause_data[1]} for clause_data in clauses_data]}
        request_data =  JSONRenderer().render(clauses)

        self.assertRaises(ValidationError, validate_and_return_wcnf, request_data)
