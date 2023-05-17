from rest_framework.response import Response


def create_response(message, status_code, data=None):
    return Response(
        data={"status_code": status_code, "message": message, "data": data},
        status=status_code,
    )
