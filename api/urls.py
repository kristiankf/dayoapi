from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubtaskViewSet, DailyLogViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'daily-logs', DailyLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]