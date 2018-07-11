from django.urls import path

from . import views

urlpatterns = [

    path('upload/', views.quotes_upload, name='quotes_upload'),
]