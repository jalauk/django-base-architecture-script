from .constants import Constant
from rest_framework.response import Response
from django.http import HttpResponse
from django_base_architecture.exception import ApiException


class Responder:

    @staticmethod
    def send(code, data=None, status=True):
        return Response(
            {
                "status": status,
                "code": code,
                "message": Constant.response_messages[code],
                "data": data if data is not None else {},
            },
            status=200 if status else 400
        )

    @staticmethod
    def sendText(code):
        return HttpResponse(Constant.response_messages[code])

    @staticmethod
    def raiseError(code):
        raise ApiException(code)
