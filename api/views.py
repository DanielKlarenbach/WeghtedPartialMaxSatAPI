# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.sat_based_wmps_solver import validate_and_return_wcnf


class WPMSSolverView(APIView):

    def post(self, request, format=None):
        wcnf = validate_and_return_wcnf(request.data)
        print(wcnf)
        return Response()
