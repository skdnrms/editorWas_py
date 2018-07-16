from django.db import models
from django.utils import timezone
from froala_editor.fields import FroalaField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    contents = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

class Page(models.Model):
    content = FroalaField()
    