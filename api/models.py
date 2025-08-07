from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    PRIORITY_WEIGHTS = {
        'high': 5,
        'medium': 3,
        'low': 1,
    }

    REPEAT_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_completed = models.BooleanField(default=False)
    repeat_type = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')
    custom_repeat_days = models.JSONField(blank=True, null=True)  # Example: ["Monday"] or [1, 15]
    date_created = models.DateField(auto_now_add=True)
    progress = models.FloatField(default=0.0)

    def get_priority_weight(self):
        return self.PRIORITY_WEIGHTS.get(self.priority, 3)

    def __str__(self):
        return f"{self.title} ({self.priority})"
    
    def update_progress(self):
        subtasks = self.subtasks.all()
        if not subtasks.exists():
            self.progress = 100.0 if self.is_completed else 0.0
        else:
            total = subtasks.count()
            completed = subtasks.filter(is_completed=True).count()
            self.progress = (completed / total) * 100.0
            if self.progress >= 100.0:
                self.is_completed = True
        self.save()
    class Meta:
        ordering = ['-date_created']



class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class DailyLog(models.Model):
    RATING_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('ok', 'OK'),
        ('poor', 'Poor'),
        
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(unique=True)
    score = models.FloatField(default=0.0)  # Completion score based on weights
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    points_possible = models.IntegerField(default=0)
    points_achieved = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    was_active = models.BooleanField(default=False)

    def get_points_possible(self):
        tasks = Task.objects.filter(user=self.user, date_created__date=self.date)
        return sum(task.get_priority_weight() for task in tasks)
    
    def get_points_achieved(self):
        tasks = Task.objects.filter(user=self.user, date_created__date=self.date)
        return sum(task.get_priority_weight() for task in tasks if task.is_completed)
    
    def get_total_tasks(self):
        return Task.objects.filter(user=self.user, date_created__date=self.date).count()
    
    def get_completed_tasks(self):
        return Task.objects.filter(user=self.user, date_created__date=self.date, is_completed=True).count()
    
    def get_score(self):
        return (self.get_points_achieved() / self.get_points_possible()) * 100

    def calculate_rating(self):
        tasks = Task.objects.filter(user=self.user, date_created__date=self.date)
        total_weight = sum(task.get_priority_weight() for task in tasks)
        completed_weight = sum(task.get_priority_weight() for task in tasks if task.is_completed)

        if total_weight == 0:
            self.rating = 'No Tasks'

        percent = (completed_weight / total_weight) * 100

        if percent >= 80:
            self.rating = 'Excellent'
        elif percent >= 65:
            self.rating = 'Good'
        elif percent >= 50:
            self.rating = 'OK'
        else:
            self.rating = 'Poor'

        self.save()


    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.rating})"
    
    class Meta:
        ordering = ['-date']

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    send_time = models.DateTimeField()
    message = models.TextField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.send_time}"