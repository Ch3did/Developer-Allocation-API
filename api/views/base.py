from rest_framework import status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..serializers.user_serializer import UserSerializer


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


class RegisterUserView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
