from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('users/register/', views.Register.as_view(), name='register'),

    # path('chat/<str:room_name>/', views.room, name='room'),
    # path('chat/<str:room_name>/',TemplateView.as_view(template_name='index.html')),
]