from rest_framework.routers import DefaultRouter

from .views import (AssignmentViewSet, DevelopersViewSet, ProjectsViewSet,
                    TechnologiesViewSet)

router = DefaultRouter()
router.register("technologies", TechnologiesViewSet)
router.register("developers", DevelopersViewSet)
router.register("projects", ProjectsViewSet)
router.register("assignment", AssignmentViewSet)

urlpatterns = router.urls
