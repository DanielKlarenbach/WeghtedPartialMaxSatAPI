import io

from rest_framework.parsers import JSONParser

from api.model_serializers import ClauseListSerializer


def validate_and_return_wcnf(data):
    stream = io.BytesIO(data)
    wcnf = JSONParser().parse(stream)
    serializer = ClauseListSerializer(data=wcnf)
    serializer.is_valid(raise_exception=True)
    return wcnf



def wmp1(solver_name, formula):
    pass
