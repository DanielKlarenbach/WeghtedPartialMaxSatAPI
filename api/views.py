# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.sat_based_wmps_solver import validate_and_return_wcnf, generate_wcnf_formula, wmp1


class WPMSSolverView(APIView):

    def post(self, request, format=None):
        clauses = validate_and_return_wcnf(request.data)
        wcnf_formula = generate_wcnf_formula(clauses)
        cost, solution, final_soft_clauses, final_hard_clauses  = wmp1(solver_name='glucose4', formula=wcnf_formula)
        response = Response()
        response.data = {'cost': cost, 'solution':solution, 'final_soft_clauses': final_soft_clauses, 'final_hard_clauses': final_hard_clauses}
        return response
