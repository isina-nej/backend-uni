from django.db import models
from apps.users.models import User
from apps.schedules.models import Schedule


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.schedule.course.title} on {self.date}"
