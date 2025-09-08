from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Grade.objects.filter(student=user)
        elif user.role == 'professor':
            return Grade.objects.filter(professor=user)
        return Grade.objects.all()  # Admin sees all
