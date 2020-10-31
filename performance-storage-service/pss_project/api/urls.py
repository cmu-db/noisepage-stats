from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pss_project.api import views

router = DefaultRouter()
router.register(r'health', views.HealthViewSet, 'health')
router.register(r'oltpbench', views.OLTPBenchViewSet, 'oltpbench')
router.register(r'microbenchmark', views.MicrobenchmarkViewSet, 'microbenchmark')
router.register(r'binary-metrics', views.BinaryMetricsViewSet, 'binary-metrics')
router.register(r'git-events', views.GitEventsViewSet, 'git-events')

urlpatterns = [
    path('', include(router.urls)),
]
