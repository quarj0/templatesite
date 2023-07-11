from django.urls import path, include

urlpatterns = [
    path('api/', include('rest_framework.urls')),
    path('api/', include('templatesapi.urls')),
]
