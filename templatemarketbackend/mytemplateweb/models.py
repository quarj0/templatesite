from django.db import models
from django.contrib.auth.models import User


def user_profile_picture_path(instance, filename):
    return f"user_profile/user_{instance.user.id}/profile_picture/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="", blank=True, null=True)
    last_name = models.CharField(max_length=100, default="", blank=True, null=True)
    email = models.EmailField(max_length=100, default="", unique=True)
    password = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=100, unique=True, default="")
    phone = models.CharField(max_length=100, default="", blank=True, null=True)
    city = models.CharField(max_length=255, default="", blank=True, null=True)
    address = models.CharField(max_length=255, default="", blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)

    def __str__(self):
        return self.user.username



class Template(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="templates/files", blank=True, null=True)
    image = models.ImageField(upload_to="templates/images")
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    download_link = models.URLField()
    author = models.CharField(max_length=100)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.template.title} - {self.user.username}"
    

class Review(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.template.title} - {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.template.title}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="categories/images")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name