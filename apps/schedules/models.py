from django.db import models
from apps.courses.models import Course
from apps.users.models import User


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)  # e.g., Room 101
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')

    def __str__(self):
        return f"{self.course.title} - {self.day_of_week} {self.start_time}-{self.end_time}"
