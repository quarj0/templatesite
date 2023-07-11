from django.urls import path
from .views import (TemplateListView, OrderView, UserRegisterView, 
                    ChangePasswordView, ResetPasswordView, 
                    UserProfile, UserLoginView)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'templatesapi'

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='registration'),
    path('login', UserLoginView.as_view(), name='login'),
    path('user/profile', UserProfile, name='user profile'),
    path('templatelist', TemplateListView.as_view(), name='template-list'),    
    path('change/password', ChangePasswordView.as_view(), name='login'),
    path('reset/password', ResetPasswordView.as_view(), name='reset password'),
    path('order', OrderView.as_view(), name='order-template'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
