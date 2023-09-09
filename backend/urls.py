from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', include('django_prometheus.urls')),
    path('', include('my_app.urls')),
]
