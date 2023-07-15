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
    upload_template,
)
from django.conf import settings
from django.conf.urls.static import static


app_name = "templatesapi"

urlpatterns = [
    path("api/token", get_csrf_token, name="get csrf token"),
    path("upload/template", upload_template, name="upload template"),
    path("account/register", UserRegisterView.as_view(), name="registration"),
    path("account/login", UserLoginView.as_view(), name="login"),
    path("account/user/profile", UserProfileView.as_view(), name="user profile"),
    path("account/change/email", ChangeEmailView.as_view(), name="change email"),
    path("templatelist", TemplateListView.as_view(), name="template-list"),
    path("templates/search", TemplateSearchView.as_view(), name="template-search"),
    path("account/change/password", ChangePasswordView.as_view(), name="login"),
    path("reset/password", ResetPasswordView.as_view(), name="reset password"),
    path(
        "reset/password/<str:uid>/<str:token>",
        ResetPasswordView.as_view(),
        name="reset password",
    ),
    path("order", OrderView.as_view(), name="order-template"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)