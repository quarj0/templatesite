from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator
from templatemarket.settings import EMAIL_HOST_USER
from .models import Template, UserProfile, Order, User
from .serializers import (
    TemplateSerializer,
    UpdateProfileSerializer,
    UserRegisterSerializer,
    OrderSerializer,
    UserProfileSerializer,
    TemplateCreatorSerializer,
)

@method_decorator(csrf_protect, name="dispatch")
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        try:
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            
            serializer.save(user=user)
            
            return Response({"success": f'{user} created successfully.'})
        except:
            return Response({"Oops!": "Something went wrong when trying to update your email. \n Please try again later."})
            
@method_decorator(csrf_protect, name="dispatch")       
@method_decorator(login_required, name="dispatch")       
class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, format=None):
        try:
            serializer = UpdateProfileSerializer(
                request.user.userprofile, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response({"Oops!": "Something went wrong when trying to update your profile.\n Please try again later."})
            
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(login_required, name="dispatch")
class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

@method_decorator(csrf_protect, name="dispatch")
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
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
        except:
            return Response({"Oops!": "Something went wrong when trying to login. \n Please try again later."})
            

@method_decorator(csrf_protect, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ChangeEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            password = request.data.get("password")
            new_email = request.data.get("new_email")
            
            user = authenticate(request, username=request.user.username, password=password)
            
            if user is not None:
                if user.is_active:
                    user.email = new_email
                    user.save()
                    return Response({"message": "Email changed successfully"})
                else:
                    return Response({"error": "Your account is disabled."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid login details supplied."}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError as e:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": "Oops! Something went wrong when trying to update your email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name="dispatch")
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        old_password = request.data.get("password")
        new_password = request.data.get("new_password")
        
        user = request.user  # Assuming you are using TokenAuthentication or SessionAuthentication
        
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"})
        else:
            return Response({"error": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name="dispatch")
class ResetPasswordView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
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
            message = f"Click the following link to reset your password: {reset_link}\nIf you did not request a password reset, please ignore this email.\nThank you,\nMy Templates"
            from_email = EMAIL_HOST_USER  # Update with your email address
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return JsonResponse({"message": "Password reset link sent to your email"})
        else:
            return JsonResponse({"error": "Your account is disabled."}, status=400)


@method_decorator(csrf_protect, name="dispatch")
@method_decorator(login_required, name="dispatch")
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




class UploadTemplateView(APIView):
    def post(self, request, format=None):
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