from django.utils import timezone
from .models import DailyLog

def mark_user_active(user):
    log, _ = DailyLog.objects.get_or_create(user=user, date=timezone.now().date())
    if not log.was_active:
        log.was_active = True
        log.save()
        