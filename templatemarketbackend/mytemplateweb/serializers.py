from rest_framework import serializers
from .models import Template, UserProfile, Order, Category, Rating, Review
import re

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__' 
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "template", "order_date", "status"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "city",
            "phone",
            "address",
            "profile_picture",
        ]
        

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        
        fields = [
            "first_name",
            "last_name",
            "email",
            "city",
            "phone",
            "address",
            "profile_picture"
        ]


class TemplateCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            "title",
            "description",
            "image",
            "file",
            "category",
            "is_free",
            "price",
        ]
        
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "password",
        ]
        
    def validate(self, data):
        if UserProfile.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        
        elif UserProfile.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', data["password"]):
            raise serializers.ValidationError("Password must contain at least 6 characters, one uppercase, one lowercase, one number and one special character")
        return data
    
    
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'