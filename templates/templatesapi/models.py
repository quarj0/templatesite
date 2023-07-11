from django.db import models
from django.contrib.auth.models import User

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

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.template.title

class Category(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Template, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name