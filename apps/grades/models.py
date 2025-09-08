from django.db import models
from apps.users.models import User
from apps.courses.models import Course


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 85.50
    grade_letter = models.CharField(max_length=2, blank=True)  # e.g., A, B
    date_assigned = models.DateField(auto_now_add=True)
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_grades')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}: {self.score}"
