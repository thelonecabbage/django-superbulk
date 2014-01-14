from django.db import models

# Create your models here.
class Invoice(models.Model):

    customer_id = models.CharField(max_length=30)
    invoice_no = models.CharField(max_length=6, primary_key=True)

class Customer(models.Model):

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)