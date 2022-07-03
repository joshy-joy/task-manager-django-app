from rest_framework.response import Response

def create_response(type, msg, code, data=None):
    if data:
        response = {"status": type, "message": msg, "data":data}
    else:
        response = {"status": type, "message": msg}
    return Response(response, status=code)