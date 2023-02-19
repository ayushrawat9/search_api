from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_questions, name='search_form'),
]