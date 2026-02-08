from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_view, name='schedule'),
    path('upcoming/', views.upcoming_schedule, name='upcoming_schedule'),
]