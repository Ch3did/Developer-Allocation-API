from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response



class HealthCheckView(views.APIView):
    """
    View para verificar o status de saúde da aplicação.
    """

    def get(self, request, *args, **kwargs):
        data = {
            "status": "ok",
            "message": "API is running",
        }
        return Response(data, status=status.HTTP_200_OK)
