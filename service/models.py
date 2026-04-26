from django.db import models
import uuid
from django.utils import timezone
from django.db import models
from staff.models import Staff
from payment.models import Payment

# Create your models here.
# This class handles the tyre services
class Service(models.Model):

    SERVICE_TYPES = [
        ("pressure", "Tyre Pressure"),
        ("puncture", "Puncture Fixing"),
        ("valve", "Valve Replacement"),
    ]

    name = models.CharField(max_length=20, choices=SERVICE_TYPES)
    vehicle_size = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Objects form the databases display the way they are save not as object
    def __str__(self):
        return f"{self.name} - UGX {self.price}"

#This class handles the  tyre service registration
class Tyre(models.Model):

    vehicle_plate = models.CharField(max_length=10, blank=False, null =False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=False)
    payment_method = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    registered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateField(default=timezone.now)

# This function allows the genertion of unique numbers for the receipt
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"TYR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

# Objects form the databases display the way they are save not as object
    def __str__(self):
        return f"{self.vehicle_plate} - {self.service.name}"


class Battery(models.Model):

    BATTERY_SERVICE = [
        ("Battery hire", "Battery Hire"),
        ("Battery sale", "Battery Sale"),
    ]

    customer_name = models.CharField(max_length=100)
    battery_type = models.CharField(max_length=20, choices=BATTERY_SERVICE, default='Battery hire')
    price = models.DecimalField(max_digits=6, decimal_places=3, null= False)
    Payment_method =models.ForeignKey(Payment, on_delete=models.CASCADE, null=False)
    registered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateField(default=timezone.now)

# This function allows the genertion of unique numbers for the receipt
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"BAT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
# This method allows the customer_name and battery_ type objects fetched from the database to display their real names not as object
    def __str__(self):
        return f"{self.customer_name} - {self.battery_type}"