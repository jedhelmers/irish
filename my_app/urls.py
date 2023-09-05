from django.urls import path
from . import views
from . import models

urlpatterns = [
    path('api/create_song/<int:user_id>/', views.create_song, name='create_song'),
    path('api/query_songs/', views.query_songs, name='query_songs'),
    path('api/translate/', views.translate, name='translate'),
]

models.populate_tags()