from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)