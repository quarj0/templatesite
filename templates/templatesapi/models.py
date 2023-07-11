from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

class Template(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='templates/images')
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    download_link = models.URLField()
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.template.title}"


class Category(models.Model):
    name = models.CharField(max_length=50, name='category name')
    description = models.TextField()
    image = models.ImageField(upload_to='categories/images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name