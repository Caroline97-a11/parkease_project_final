import uuid  
from django.db import models 
from django.utils import timezone 
from staff.models import Staff  


# This model stores predefined tyre service types and fixed prices
class Service(models.Model):

    # List of available tyre service types
    SERVICE_TYPES = [
        ("pressure", "Tyre Pressure"),
        ("puncture", "Puncture Fixing"),
        ("valve", "Valve Replacement"),
    ]

    name = models.CharField(max_length=20, choices=SERVICE_TYPES, unique=True)  # Service type
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Service price

    # Human-readable display of service
    def __str__(self):
        return f"{self.get_name_display()} - UGX {self.price}"


# This model records tyre service transactions
class Tyre(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("mobile_money", "Mobile Money"),
        ("card", "Card"),
    ]

    vehicle_plate = models.CharField(max_length=10)  # Vehicle registration number

    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Linked service

    vehicle_size = models.CharField(max_length=50, null=True, blank=True)  # Optional tyre size
    model = models.CharField(max_length=50, null=True, blank=True)  # Optional vehicle model

    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES,null=True,blank=True)

    registered_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True
    )  # Staff who registered record

    receipt_number = models.CharField(max_length=20, unique=True, editable=False)  # Auto-generated receipt

    date = models.DateTimeField(default=timezone.now)  # Date of record

    # Generate unique receipt number before saving
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"TYR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    # Display format
    def __str__(self):
        return f"{self.vehicle_plate} - {self.service.name}"


# This model records battery service transactions
class Battery(models.Model):

    # Battery service types
    BATTERY_SERVICE = [
        ("hire", "Battery Hire"),
        ("sale", "Battery Sale"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("mobile_money", "Mobile Money"),
        ("card", "Card"),
    ]

    customer_name = models.CharField(max_length=100)

    battery_type = models.CharField(max_length=20, choices=BATTERY_SERVICE) 

    price = models.DecimalField(max_digits=10, decimal_places=2) 

    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES,null=True,blank=True)
    registered_by = models.ForeignKey(Staff,on_delete=models.SET_NULL,null=True) 

    receipt_number = models.CharField(max_length=20, unique=True, editable=False)  # Receipt ID

    date = models.DateTimeField(default=timezone.now) 

    # Auto-generate receipt number
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"BAT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    # Display format
    def __str__(self):
        return f"{self.customer_name} - {self.battery_type}"