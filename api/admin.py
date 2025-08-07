from django.contrib import admin
from .models import Task, SubTask, DailyLog, Notification

# Register your models here.
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(DailyLog)
admin.site.register(Notification)