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
    # path('', views.CustomTemplateView.as_view(), name='home'),
    # re_path(r'^.*', views.index, name='index'),
    # re_path(r'^metrics/(?P<path>.*)$', ProxyView.as_view(upstream='http://prometheus:9090/')),
    # re_path(r'^prometheus/.*$', views.prometheus_reverse_proxy),
    

    # re_path(r'^metrics/$', ProxyView.as_view(upstream='http://localhost:9090')),
    # re_path(r'^prometheus/(?P<path>.*)$', ProxyView.as_view(upstream='http://localhost:9090')),
    # path('metrics/', ProxyView.as_view(upstream='http://localhost:9090')),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
    # re_path(r'^.*', TemplateView.as_view(template_name='frontend/build/index.html')),
]

print('urlpatterns', urlpatterns)