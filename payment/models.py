from django.db import models

# Create your models here.
class Payment(models.Model):
    PAYMENT_CHOICE = [
        ('mobile money', 'Mobile money'),
          ('cash','Cash'),
          ('card','Card')
          ]
    Payment_method =models.CharField(max_length=20, choices=PAYMENT_CHOICE, default='Cash')