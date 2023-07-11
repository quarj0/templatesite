from rest_framework import generics
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Template
from .serializers import TemplateSerializer, UserSerializer, OrderSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserRegisterView(generics.CreateAPIView):
    queryset = Template.objects.all()
    serializer_class = UserSerializer

    
    @csrf_exempt
    def user_login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'message': 'Login successful'})
                else:
                    return JsonResponse({'error': 'Your account is disabled.'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid login details supplied.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    @csrf_exempt
    def change_password(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
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
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    
            
    @csrf_exempt
    def reset_password(request):
        if request.method == "POST":
            email = request.POST.get('email')
            user = User.objects.get(email=email)
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
    queryset = Template.objects.all()
    serializer_class = OrderSerializer

