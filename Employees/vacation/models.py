from django.db import models
from django.utils import timezone
from django.forms import widgets

class CustomUserModel(models.Model):    
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    confirmpassword = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    
class Vacation(models.Model):
    employee = models.ForeignKey('auth.User')    
    description = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    from_date = models.DateField()
    to_date = models.DateField()
    
    def __str__(self):
        return self.description
     
