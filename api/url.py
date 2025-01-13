from rest_framework.routers import DefaultRouter

from .views import (AlocacaoViewSet, ProgramadorViewSet, ProjetoViewSet,
                    TecnologiaViewSet)

router = DefaultRouter()
router.register("tecnologias", TecnologiaViewSet)
router.register("programadores", ProgramadorViewSet)
router.register("projetos", ProjetoViewSet)
router.register("alocacoes", AlocacaoViewSet)

urlpatterns = router.urls
