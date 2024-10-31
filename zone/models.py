from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Genres"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    genre = models.ForeignKey(Genre, related_name="books", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()

    is_sold = models.BooleanField(default=False)
    stock = models.IntegerField()

    created_by = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.name

