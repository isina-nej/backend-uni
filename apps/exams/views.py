from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Exam
from .serializers import ExamSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Exam.objects.filter(course__students=user)
        elif user.role == 'professor':
            return Exam.objects.filter(professor=user)
        return Exam.objects.all()
