from django.contrib import admin
from django.urls import path, include
from my_app import views
from django.urls import re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', include('django_prometheus.urls')),
    path('api/', include('my_app.urls')),
    # path('', views.CustomTemplateView.as_view(), name='home'),
    # re_path(r'^.*', views.index, name='index'),
    # re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
    re_path(r'^.*', TemplateView.as_view(template_name='frontend/build/index.html')),
]
