from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Staff


# =========================
# STAFF REGISTRATION FORM
# =========================
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

    # =========================
    # VALIDATIONS
    # =========================

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            if Staff.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already used.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
            if len(username) < 4:
                raise forms.ValidationError("Username must be at least 4 characters.")
        return username


# =========================
# STAFF LOGIN FORM
# =========================
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