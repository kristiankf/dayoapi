from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SubTask

@receiver(post_save, sender=SubTask)
def update_task_progress_on_save(sender, instance, **kwargs):
    instance.task.update_progress()

@receiver(post_delete, sender=SubTask)
def update_task_progress_on_delete(sender, instance, **kwargs):
    instance.task.update_progress()