from django.urls import path
from . import views


urlpatterns = [
    path('api/create_song/<int:user_id>/', views.create_song, name='create_song'),
    path('api/query_songs/', views.query_songs, name='query_songs'),
    path('api/translate/', views.translate_view, name='translate'),
    path('api/check_task_status/<str:task_id>/', views.check_task_status, name='check_task_status'),
    path('api/test/<str:test_string', views.test, name='test'),
]
