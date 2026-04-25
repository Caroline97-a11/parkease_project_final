from django.db import models
from django.db import models
import uuid
from django.utils import timezone
from staff.models import Staff
from payment.models import Payment

# Create your models here.
# class for vehicle category
class Category(models.Model):

    VEHICLE_TYPES = [
        ("Truck", "truck"),
        ("Personal car", "personal car"),
        ("Taxi", "taxi"),
        ("coaster", "coaster"),
        ("Boda-boda", "boda-boda"),
    ]

    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES, unique=True)

    day_rate = models.IntegerField()
    night_rate = models.IntegerField()
    short_stay_rate = models.IntegerField()

    def __str__(self):
        return self.vehicle_type

# class for vehicle registration
class Registration(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    STATUS_CHOICES = [
        ('parked', 'Parked'),
        ('signed_out', 'Signed Out')
    ]

    RATE_TYPE_CHOICES = [
        ("day", "Day"),
        ("night", "Night"),
        ("short", "Short Stay"),
    ]

    vehicle_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=10)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100, null=True,blank=True)
    driver_name = models.CharField(max_length=100, null=True,blank=True)
    driver_status = models.CharField(max_length=10,choices=GENDER_CHOICES,null=True,blank=True )
    phone_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    arrival_time = models.DateTimeField(default=timezone.now)
    departure_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="parked")
    ticket_number = models.CharField( max_length=20, unique=True,editable=False)
    fee = models.IntegerField(default=0)
    rate_type = models.CharField(max_length=10,choices=RATE_TYPE_CHOICES,null=True,blank=True)
    pyment_method = models.ForeignKey(Payment, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(Staff,on_delete=models.SET_NULL,null=True)

# This allows for unique ticket numbers
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

# Objects form the databases display the way they are save not as object
    def __str__(self):
        return f"{self.plate_number} ({self.ticket_number})"