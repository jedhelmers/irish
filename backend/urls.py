from django.contrib import admin
from django.urls import path, include
from my_app import views
from django.urls import re_path
from django.views.generic import TemplateView
from revproxy.views import ProxyView


urlpatterns = [
    path('monitoring/', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('my_app.urls')),
    path('grafana/', views.grafana_proxy, name='grafana_proxy'),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]
