from django.db import models
from apps.users.models import User


class Notification(models.Model):
    PLATFORM_CHOICES = [
        ('web', 'Web'),
        ('flutter', 'Flutter App'),
        ('telegram', 'Telegram Bot'),
        ('discord', 'Discord Bot'),
        ('slack', 'Slack Bot'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.title}"
