from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class for staff/ users
class Staff(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('ATTENDANT', 'Attendant'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='ADMIN')
    created_at = models.DateField(default=timezone.now)

# Objects form the databases display the way they are save not as object
    def __str__(self):
        return self.username