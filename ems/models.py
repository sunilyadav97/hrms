from django.db import models


class Department(models.Model):
    name=models.CharField(max_length=70)
    description=models.TextField(max_length=200)
    
class Role(models.Model):
    name=models.CharField(max_length=70)
    description=models.TextField(max_length=200)

