from django.db import models

# Create your models here.


class UserMok(models.Model):

    first_name = models.CharField(max_length=5)
    last_name = models.CharField(max_length=10)
    password = models.CharField(max_length=2)

class Invoice(models.Model):

    customer_id = models.CharField(max_length=30)
    invoice_no = models.CharField(max_length=6, primary_key=True)

class Customer(models.Model):

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)