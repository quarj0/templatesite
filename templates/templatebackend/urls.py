from django.urls import path, include

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('account/', include('templatesapi.urls')),
]
