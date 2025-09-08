from django.db import models
from apps.courses.models import Course
from apps.users.models import User


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')

    def __str__(self):
        return f"{self.title} - {self.course.title} on {self.date}"
