from django import forms
from vehicle.models import Category, Registration
import re


# category form logic
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


# form for registering a new vehicle
class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = [
            "vehicle_type",
            "plate_number",
            "model",
            "color",
            "driver_name",
            "driver_status",
            "phone_number",
            "nin_number",
        ]

        widgets = {
            "vehicle_type": forms.Select(attrs={"class": "form-select"}),
            "plate_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. UA123A"
            }),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "driver_status": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+2567XXXXXXXX"
            }),
            "nin_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "CXXXXXXXXXXXX"
            }),
        }

   # validating the driver name
    def clean_driver_name(self):
        name = self.cleaned_data.get("driver_name")

        if not name:
            raise forms.ValidationError("Driver name is required.")

        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")

        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain letters only.")

        if not name[0].isupper():
            raise forms.ValidationError("Name must start with a capital letter.")

        return name.title()

# phone validation to match ugandan format
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            raise forms.ValidationError("Phone number is required.")

        if not phone.startswith("+256"):
            raise forms.ValidationError("Phone must start with +256.")

        if not phone[1:].isdigit():
            raise forms.ValidationError("Phone must contain digits only after +.")

        if len(phone) != 13:
            raise forms.ValidationError("Phone must be +256XXXXXXXXX.")

        return phone

# number plate checks
    def clean_plate_number(self):
        plate = self.cleaned_data.get("plate_number")

        if not plate:
            raise forms.ValidationError("Plate number is required.")

        plate = plate.upper()

        if not plate.startswith("U"):
            raise forms.ValidationError("Plate must start with 'U'.")

        if not plate.isalnum():
            raise forms.ValidationError("Plate must be alphanumeric only.")

        if len(plate) > 6:
            raise forms.ValidationError("Plate must not exceed 6 characters.")

        return plate

 #nin number validation checks
    def clean_nin_number(self):
        nin = self.cleaned_data.get("nin_number")

        if nin:
            nin = nin.upper()

            if not nin.startswith("C"):
                raise forms.ValidationError("NIN must start with 'C'.")

            if len(nin) not in [13, 14]:
                raise forms.ValidationError("NIN must be 13 or 14 characters.")

            if not nin.isalnum():
                raise forms.ValidationError("NIN must be alphanumeric only.")

        return nin

 # form validation
    def clean(self):
        cleaned_data = super().clean()

        vehicle_type = cleaned_data.get("vehicle_type")
        nin_number = cleaned_data.get("nin_number")

        # boda rule checking
        if vehicle_type and vehicle_type.vehicle_type == "Boda-boda":
            if not nin_number:
                self.add_error("nin_number", "NIN is required for Boda-boda drivers.")

        return cleaned_data


# sign out form logic
class CheckOutForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ["driver_name", "phone_number", "nin_number", "driver_status", "payment_method"]

        widgets = {
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "nin_number": forms.TextInput(attrs={"class": "form-control"}),
            "driver_status": forms.Select(attrs={"class": "form-select"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }


