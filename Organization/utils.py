from rest_framework.response import Response

def build_response(status, message, data, **kargs):
    response_result ={
        "status":status,
        "message": message,
        "data":data,
        **kargs
    }
    return Response(response_result)