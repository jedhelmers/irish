from django.urls import path
from my_app import views
from django.urls import re_path
from django.views.generic import TemplateView


urlpatterns = [
    path('translate/', views.translate_view, name='translate'),
    path('add_tags/<int:query_id>/', views.add_tags_to_userquery, name='add_tags_to_userquery'),
    path('remove_tags/<int:query_id>/', views.remove_tags_from_userquery, name='remove_tags_from_userquery'),
    path('remove_query/<int:query_id>/', views.remove_userquery, name='remove_userquery'),
    path('get_queries/<int:user_id>/', views.get_userqueries, name='get_userqueries'),
    path('tags/', views.get_all_tags, name='get_all_tags'),
    path('submit_guess/', views.submit_guess, name='submit_guess'),

]
