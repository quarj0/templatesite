from django.core.mail import send_mail
from templatebackend.settings import EMAIL_HOST_USER
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Template, UserProfile, Order, User
from .serializers import TemplateSerializer, UserSerializer, OrderSerializer, UserProfileSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    
    
    def perform_create(self, serializer):
        user = User.objects.create_user(
            username = serializer.validated_data['username'],
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password'],
        )
        
        serializer.save(user=user)
        

class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile
    
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Your account is disabled.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid login details supplied.'}, status=400)


class ChangeEmailView(APIView):
    def post(self, request):
        password = request.data.get('password')
        new_email = request.data.get('new_email')
        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            if user.is_active:
                user.email = new_email
                user.save()
                return JsonResponse({'message': 'Email changed successfully'})
            else:
                return JsonResponse({'error': 'Your account is disabled.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid login details supplied.'}, status=400)



class ChangePasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        old_password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = authenticate(request, username=username, password=old_password)
        if user is not None:
            if user.is_active:
                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password changed successfully'})
            else:
                return JsonResponse({'error': 'Your account is disabled.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid login details supplied.'}, status=400)


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid login details supplied.'}, status=400)

        if user.is_active:
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).encode('utf-8').decode()

            # Build the password reset link
            current_site = get_current_site(request)
            reset_link = f"http://{current_site.domain}/reset-password/{uid}/{token}/"

            # Send the email
            subject = 'Password Reset'
            message = f'Click the following link to reset your password: {reset_link}'
            from_email = EMAIL_HOST_USER # Update with your email address
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return JsonResponse({'message': 'Password reset link sent to your email'})
        else:
            return JsonResponse({'error': 'Your account is disabled.'}, status=400)


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
        title = self.request.query_params.get('title', None)
        category = self.request.query_params.get('category', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if category is not None:
            queryset = queryset.filter(category__icontains=category)
        return queryset    



def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
