from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_leave, name='create_leave'),
    path('', views.leave_list, name='leave_list'),
    path('<int:pk>/cancel/', views.cancel_leave, name='cancel_leave'),
]