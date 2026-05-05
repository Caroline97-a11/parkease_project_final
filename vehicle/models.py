from django.db import models
import uuid
from django.utils import timezone
from staff.models import Staff


# =========================
# CATEGORY MODEL
# =========================

class Category(models.Model):
    """
    Stores vehicle types and their parking rates
    """

    VEHICLE_TYPES = [
        ("Truck", "Truck"),
        ("Personal car", "Personal car"),
        ("Taxi", "Taxi"),
        ("Coaster", "Coaster"),
        ("Boda-boda", "Boda-boda"),
    ]

    vehicle_type = models.CharField(
        max_length=50,
        choices=VEHICLE_TYPES,
        unique=True
    )

    day_rate = models.IntegerField()
    night_rate = models.IntegerField()
    short_stay_rate = models.IntegerField()

    def __str__(self):
        return self.vehicle_type


# =========================
# VEHICLE REGISTRATION MODEL
# =========================

class Registration(models.Model):
    """
    Stores all parked vehicles information
    """

    # Gender choices for driver
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female")
    ]

    # Vehicle status
    STATUS_CHOICES = [
        ("parked", "Parked"),
        ("signed_out", "Signed Out")
    ]

    # Rate types
    RATE_TYPE_CHOICES = [
        ("day", "Day"),
        ("night", "Night"),
        ("short", "Short Stay"),
        ("overstay", "Overstay"),
    ]

    # Payment options
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("mobile_money", "Mobile Money"),
        ("card", "Card"),
    ]

    # Vehicle type
    vehicle_type = models.ForeignKey(Category, on_delete=models.CASCADE)

    plate_number = models.CharField(max_length=10)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100, null=True, blank=True)

    driver_name = models.CharField(max_length=100, null=True, blank=True)
    driver_status = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    phone_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, null=True, blank=True)

    arrival_time = models.DateTimeField(default=timezone.now)
    departure_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="parked"
    )

    ticket_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    rate_type = models.CharField(
        max_length=10,
        choices=RATE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True
    )

    registered_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True
    )

    # =========================
    # AUTO GENERATE TICKET NUMBER
    # =========================
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    # =========================
    # CALCULATE PARKING FEE
    # =========================
    def calculate_fee(self):
        """
        Calculates parking fee based on time stayed
        Returns: (fee, rate_type)
        """

        now = timezone.now()
        duration = (now - self.arrival_time).total_seconds() / 3600  # hours
        category = self.vehicle_type

        # SHORT STAY
        if duration < 3:
            return category.short_stay_rate, "short"

        # NORMAL DAY / NIGHT (same day)
        elif duration <= 24:
            arrival_hour = timezone.localtime(self.arrival_time).hour

            if 6 <= arrival_hour < 19:
                return category.day_rate, "day"
            else:
                return category.night_rate, "night"

        # OVERSTAY (MORE THAN 1 DAY)
        else:
            extra_days = int(duration // 24)
            remaining_hours = duration % 24

            fee = category.day_rate * extra_days

            if remaining_hours < 3:
                fee += category.short_stay_rate
            else:
                fee += category.day_rate

            return fee, "overstay"

    def __str__(self):
        return f"{self.plate_number} ({self.ticket_number})"