from django.urls import path

from . import views

urlpatterns = [

    path('upload/', views.quotes_upload, name='quotes_upload'),
    path('materials_upload/', views.quoted_materials_upload, name='quoted_materials_upload'),
    path('manage/', views.quotes_manager, name='quotes_manager'),
    path('manage/edit/<str:code>', views.quotes_material_editor, name='quotes_editor'),
]