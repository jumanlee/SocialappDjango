from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('chat/', TemplateView.as_view(template_name='index.html')),
    # path('chat/<str:room_name>/', views.room, name='room'),
    # path('chat/<str:room_name>/',TemplateView.as_view(template_name='index.html')),
]