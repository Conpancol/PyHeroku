from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.simple_upload, name='simple_upload'),
]