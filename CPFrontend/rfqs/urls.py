from django.urls import path

from . import views

urlpatterns = [

    path('upload/', views.rfq_upload, name='rfq_upload'),
    path('download/', views.rfq_export, name='rfq_export'),
    path('quotefinder/', views.rfq_qfinder, name='rfq_qfinder'),

]
