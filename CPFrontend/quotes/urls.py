from django.urls import path

from . import views

urlpatterns = [

    path('upload/', views.quotes_upload, name='quotes_upload'),
    path('materials_upload/', views.quoted_materials_upload, name='quoted_materials_upload'),
]