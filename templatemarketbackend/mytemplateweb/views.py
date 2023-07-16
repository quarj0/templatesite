from django.core.mail import send_mail
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import re
from django.utils.decorators import method_decorator
from templatemarket.settings import EMAIL_HOST_USER
from .models import Template, UserProfile, Order, User
from .serializers import (
    TemplateSerializer,
    UpdateProfileSerializer,
    UserSerializer,
    OrderSerializer,
    UserProfileSerializer,
    TemplateCreatorSerializer,
)


@method_decorator(csrf_exempt, name="dispatch")
class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    
    def post(self, request, format=None):
        data = request.data
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        # Validate username
        if not re.match(r'^[a-zA-Z0-9_]{4,20}$', username):
            return Response({"error": "Username must be 4-20 characters long and can only contain letters, numbers, and underscores."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email address already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            return Response({"error": "Password must contain at least one lowercase letter, one uppercase letter, one numeric character, one special character, and be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Serialize user data
        serializer = self.serializer_class(user)
        
        # Return success response
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateProfileView(generics.UpdateAPIView):
    def put(self, request, format=None):
        serializer = UpdateProfileSerializer(
            request.user.userprofile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Your account is disabled."}, status=400)
        else:
            return JsonResponse(
                {"error": "Invalid login details supplied."}, status=400
            )


class ChangeEmailView(APIView):
    def post(self, request):
        password = request.data.get("password")
        new_email = request.data.get("new_email")
        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            if user.is_active:
                user.email = new_email
                user.save()
                return JsonResponse({"message": "Email changed successfully"})
            else:
                return JsonResponse({"error": "Your account is disabled."}, status=400)
        else:
            return JsonResponse(
                {"error": "Invalid login details supplied."}, status=400
            )


class ChangePasswordView(APIView):
    def post(self, request):
        username = request.data.get("username")
        old_password = request.data.get("password")
        new_password = request.data.get("new_password")
        user = authenticate(request, username=username, password=old_password)
        if user is not None:
            if user.is_active:
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message": "Password changed successfully"})
            else:
                return JsonResponse({"error": "Your account is disabled."}, status=400)
        else:
            return JsonResponse(
                {"error": "Invalid login details supplied."}, status=400
            )


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid login details supplied."}, status=400
            )

        if user.is_active:
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).encode("utf-8").decode()

            # Build the password reset link
            current_site = get_current_site(request)
            reset_link = f"http://{current_site.domain}/reset-password/{uid}/{token}/"

            # Send the email
            subject = "Password Reset"
            message = f"""Click the following link to reset your password: {reset_link}\n
            If you did not request a password reset, please ignore this email.\n
            Thank you,\n
            My Templates
            """
            from_email = EMAIL_HOST_USER  # Update with your email address
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return JsonResponse({"message": "Password reset link sent to your email"})
        else:
            return JsonResponse({"error": "Your account is disabled."}, status=400)


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TemplateListView(generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateSearchView(generics.ListAPIView):
    serializer_class = TemplateSerializer

    def get_queryset(self):
        queryset = Template.objects.all()
        title = self.request.query_params.get("title", None)
        category = self.request.query_params.get("category", None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if category is not None:
            queryset = queryset.filter(category__icontains=category)
        return queryset


@csrf_exempt
@api_view(["POST"])
def upload_template(request):
    serializer = TemplateCreatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    title = request.data.get("title")
    description = request.data.get("description")
    category = request.data.get("category")
    image = request.FILES.get("image")
    file = request.FILES.get("file")
    is_free = request.data.get("is_free")
    price = request.data.get("price")

    # Perform file type validation
    allowed_extensions = [
        ".html",
        ".htm",
        ".zip",
        "jpeg",
        "jpg",
        "png",
    ]  # Add other allowed file extensions as needed

    file_extension = default_storage.get_extension(file.name)
    if file_extension not in allowed_extensions:
        return Response(
            {
                "error": "Invalid file type. Accepted file types are: html, htm, zip, jpeg, jpg, png."
            },
            status=400,
        )

    # Additional security measures can be implemented here, such as scanning for malicious code or using antivirus checks
    try:
        # Check if the file is contians malicious code
        pass
    except:
        pass
    # Save the template if it passes the validation
    try:
        template = Template(
            title=title,
            description=description,
            file=file,
            image=image,
            category=category,
            is_free=is_free,
            price=price,
        )
        template.full_clean()  # Validate model fields
        template.save()
    except ValidationError as e:
        return Response({"error": e}, status=400)

    return Response({"message": "Template uploaded successfully"})


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})