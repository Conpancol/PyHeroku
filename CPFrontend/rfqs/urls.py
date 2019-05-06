from django.urls import path

from . import views

urlpatterns = [

    path('upload/', views.rfq_upload, name='rfq_upload'),
    path('download/', views.rfq_export, name='rfq_export'),
    path('quotefinder/', views.rfq_qfinder, name='rfq_qfinder'),
    path('manage/', views.rfq_manager, name='rfq_manager'),
    path('manage/edit/<str:code>', views.rfq_material_editor_test, name='rfq_editor'),
    path('manage/material_reload/<str:code>', views.rfq_material_reload, name='rfq_material_reload'),
    path('manage/analyze/<str:code>', views.rfq_basic_analyzer, name='rfq_basic_analyzer')

]
