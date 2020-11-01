from django.db import models
from django.contrib.auth.models import User

class customuser(models.Model):
    plan_choices = (
        ('free','free'),
        ('paid','paid'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=500, unique=True)
    shop_api_key = models.CharField(max_length=500, unique=True)
    shop_password = models.CharField(max_length=500, unique=True)
    plan = models.CharField(max_length=500, choices=plan_choices)
    date = models.DateTimeField(blank=True, null=True)