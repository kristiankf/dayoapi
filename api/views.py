from rest_framework import viewsets, permissions
from .models import Task, SubTask, DailyLog
from .serializers import TaskSerializer, SubTaskSerializer, DailyLogSerializer
from .utils import mark_user_active

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.tasks.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        mark_user_active(self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        mark_user_active(self.request.user)
    
    def perform_destroy(self, instance):
        instance.delete()
        mark_user_active(self.request.user)

class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(task__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(task__user=self.request.user)
        mark_user_active(self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()
        mark_user_active(self.request.user)
    

class DailyLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.daily_logs.all()