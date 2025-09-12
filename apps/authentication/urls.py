from django.urls import path
from . import views
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def auth_root(request):
    return Response({'message': 'Authentication API', 'endpoints': ['login/', 'logout/', 'profile/']})

urlpatterns = [
    path('', auth_root, name='auth_root'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
]
