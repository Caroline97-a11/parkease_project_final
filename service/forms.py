from django import forms
from .models import Service, Tyre, Battery
import re


# service price form
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


# trye service form
class TyreAddForm(forms.ModelForm):

    class Meta:
        model = Tyre
        fields = '__all__'

        widgets = {
            "vehicle_plate": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. UAB123"
            }),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'registered_by': forms.Select(attrs={'class': 'form-select'}),
        }

   # plate validation
    def clean_vehicle_plate(self):
        plate = self.cleaned_data.get("vehicle_plate")

        if not plate:
            raise forms.ValidationError("Vehicle plate is required.")

        plate = plate.upper()

        # Must start with U
        if not plate.startswith("U"):
            raise forms.ValidationError("Plate must start with 'U'.")

        # Must be alphanumeric
        if not plate.isalnum():
            raise forms.ValidationError("Plate must be alphanumeric only.")

        # Length rule (realistic improvement for Uganda plates)
        if len(plate) > 7:
            raise forms.ValidationError("Plate must not exceed 7 characters.")

        return plate


# Battery form logic 
class BatteryAddForm(forms.ModelForm):

    class Meta:
        model = Battery
        fields = [
            "customer_name",
            "battery_type",
            "price",
            "Payment_method",
            "registered_by"
        ]

        widgets = {
            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Customer name"
            }),
            "battery_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "Payment_method": forms.Select(attrs={"class": "form-select"}),
            "registered_by": forms.Select(attrs={"class": "form-select"}),
        }

 # validating the customer name
    def clean_customer_name(self):
        name = self.cleaned_data.get("customer_name")

        if not name:
            raise forms.ValidationError("Customer name is required.")

        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")

        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain letters only.")

        if not name[0].isupper():
            raise forms.ValidationError("Name must start with a capital letter.")

        return name.title()

   # price amount validation
    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is None:
            raise forms.ValidationError("Price is required.")

        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")

        return price