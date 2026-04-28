from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Staff


# STAFF REGISTRATION FORM
class StaffForm(UserCreationForm):

    class Meta:
        model = Staff
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'role',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    # Password styling
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # VALIDATIONS
def clean(self):
    cleaned_data = super().clean()

    first_name = cleaned_data.get("first_name")
    last_name = cleaned_data.get("last_name")
    email = cleaned_data.get("email")
    username = cleaned_data.get("username")

    # FIRST NAME VALIDATION
    if first_name:
        if len(first_name) < 3:
            self.add_error("first_name", "First name must be at least 3 characters.")

        if any(char.isdigit() for char in first_name):
            self.add_error("first_name", "First name must not contain numbers.")


    # LAST NAME VALIDATION
 
    if last_name:
        if len(last_name) < 3:
            self.add_error("last_name", "Last name must be at least 3 characters.")

        if any(char.isdigit() for char in last_name):
            self.add_error("last_name", "Last name must not contain numbers.")

    
    # EMAIL VALIDATION

    if email:
        email = email.lower()
        cleaned_data["email"] = email

        if Staff.objects.filter(email=email).exists():
            self.add_error("email", "This email is already used.")

   
    # USERNAME VALIDATION

    if username:
        username = username.lower()
        cleaned_data["username"] = username

        if len(username) < 4:
            self.add_error("username", "Username must be at least 4 characters.")

    return cleaned_data


# STAFF LOGIN FORM

class StaffLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )