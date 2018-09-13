from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.simple_upload, name='simple_upload'),
    path('singlexcheck/', views.singlexcheck, name='singlexcheck'),
    path('multiplexcheck/', views.multiplexcheck, name='multiplexcheck'),
    path('manage/', views.material_manager, name='material_manager'),
    path('manage/edit/<str:code>', views.material_editor, name='material_editor'),

]