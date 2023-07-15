from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='', blank=True, null=True)
    last_name = models.CharField(max_length=100, default='', blank=True, null=True)
    phone = models.CharField(max_length=100, default='', blank=True, null=True)
    city = models.CharField(max_length=255, default='', blank=True, null=True)
    address = models.CharField(max_length=255, default='', blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Template(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='templates/images')
    category = models.CharField(max_length=50, name='category')
    created_at = models.DateTimeField(auto_now_add=True)
    download_link = models.URLField()
    author = models.CharField(max_length=100)
    is_free = models.BooleanField(default=True)
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
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name