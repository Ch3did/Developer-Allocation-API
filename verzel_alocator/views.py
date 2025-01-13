from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Descrição da sua API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="suporte@exemplo.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


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
