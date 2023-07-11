from django.urls import path
from .views import TemplateList
from django.conf import settings
from django.conf.urls.static import static

app_name = 'templatesapi'

urlpatterns = [
    path('templatesapi/', TemplateList.as_view(), name='template-list'),    
    # Add other URLs for your project here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
