from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.simple_upload, name='simple_upload'),
    path('list/', views.list_all, name='list_all'),
    path('manage/', views.provider_manager, name='provider_manager'),
    path('manage/edit/<str:code>', views.provider_editor, name='provider_editor'),
    path('manage/comment/<str:code>', views.provider_comment, name='provider_comment'),
]
