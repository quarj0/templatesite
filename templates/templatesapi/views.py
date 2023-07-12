from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Template, UserProfile, Order
from .serializers import TemplateSerializer, UserSerializer, OrderSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserLoginView(APIView):
    @csrf_exempt
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

class ChangePasswordView(APIView):
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
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
    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        user = UserProfile.objects.get(email=email)
        if user is not None:
            if user.is_active:
                # Generate a password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
                
                # Build the password reset link
                current_site = get_current_site(request)
                reset_link = f"http://{current_site.domain}/reset-password/{uid}/{token}/"
                
                return JsonResponse({'reset_link': reset_link})
            else:
                return JsonResponse({'error': 'Your account is disabled.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid login details supplied.'}, status=400)

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
            queryset = queryset.filter(category__name__icontains=category)
        return queryset
        