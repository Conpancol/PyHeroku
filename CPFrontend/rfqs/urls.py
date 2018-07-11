from django.urls import path

from . import views

urlpatterns = [

    path('upload/', views.rfq_upload, name='rfq_upload'),
]