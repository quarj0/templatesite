from django.db import models

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
