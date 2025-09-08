from django.db import models
from apps.users.models import User


class ResearchProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    lead_researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    team_members = models.ManyToManyField(User, related_name='research_projects')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('paused', 'Paused')
    ], default='ongoing')

    def __str__(self):
        return self.title
