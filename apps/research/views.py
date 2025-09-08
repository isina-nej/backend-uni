from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ResearchProject
from .serializers import ResearchProjectSerializer


class ResearchProjectViewSet(viewsets.ModelViewSet):
    queryset = ResearchProject.objects.all()
    serializer_class = ResearchProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'professor':
            return ResearchProject.objects.filter(lead_researcher=user) | ResearchProject.objects.filter(team_members=user)
        return ResearchProject.objects.all()
