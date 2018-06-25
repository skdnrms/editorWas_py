from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    contents = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)