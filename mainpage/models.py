from django.db import models

# Create your models here.

class Questions(models.Model):
    question = models.CharField(max_length=255, unique=True, primary_key=True)
    skill = models.CharField(max_length=255)
    model_answer = models.CharField(max_length=2000)