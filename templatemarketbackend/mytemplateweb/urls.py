from django.urls import path
from .views import (
    TemplateListView,
    OrderView,
    UserRegisterView,
    ChangePasswordView,
    ResetPasswordView,
    UserProfileView,
    UserLoginView,
    TemplateSearchView,
    get_csrf_token,
    ChangeEmailView,
    UploadTemplateView,
    UpdateProfileView,
)
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "templatesapi"

urlpatterns = [
    path("api/token", get_csrf_token, name="get csrf token"),
    path("upload/template", UploadTemplateView.as_view(), name="upload template"),
    path("account/update/profile", UpdateProfileView.as_view(), name="update profile"),
    path("account/register", UserRegisterView.as_view(), name="registration"),
    path("account/login", UserLoginView.as_view(), name="login"),
    path("account/user/profile", UserProfileView.as_view(), name="user profile"),
    path("account/change/email", ChangeEmailView.as_view(), name="change email"),
    path("account/change/password", ChangePasswordView.as_view(), name="login"),
    path("template/list", TemplateListView.as_view(), name="template-list"),
    path("templates/search", TemplateSearchView.as_view(), name="template-search"),
    path("password/reset", ResetPasswordView.as_view(), name="reset password"),
    path("password/reset/<str:uid>/<str:token>/", ResetPasswordView.as_view(), name="reset password"),
    path("order", OrderView.as_view(), name="order-template"),
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template-detail'),
    path('templates/<int:pk>/rate/', views.TemplateRatingView.as_view(), name='template-rate'),
    path('templates/<int:pk>/review/', views.TemplateReviewView.as_view(), name='template-review'),
    path('account/logout', views.UserLogoutView.as_view(), name='logout'),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)