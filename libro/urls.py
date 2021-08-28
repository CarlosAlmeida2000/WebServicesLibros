from django.urls import path
from . import views

urlpatterns = [
    path('libro/', views.Libro.as_view()),
]