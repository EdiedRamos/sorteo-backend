from django.db import models

# Create your models here.
class Company(models.Model):
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=50)
  nit = models.CharField(max_length=50)
  phone = models.CharField(max_length=50)