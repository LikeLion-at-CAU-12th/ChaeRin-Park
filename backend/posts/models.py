from django.db import models

# Create your models here.
class codeReview(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(default="", max_length=30)
    age = models.IntegerField(default=0)
    major = models.CharField(default="", max_length=30)
    github = models.CharField(default="", max_length=30)