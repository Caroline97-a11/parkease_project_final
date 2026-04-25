from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Staff


class StaffForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        error_messages={
            'required': 'Username is required.',
            'max_length': 'Username is too long.'
        }
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        error_messages={
            'required': 'Password is required.'
        }
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        error_messages={
            'required': 'Please confirm your password.'
        }
    )

    class Meta:
        model = Staff
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'role',
            'created_at',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@gmail.com'
            }),

            'role': forms.Select(attrs={
                'class': 'form-control'
            }),

            'created_at': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
# hand;ing error messages that show on each field
        error_messages = {
            'first_name': {
                'required': 'First name is required.',
            },
            'last_name': {
                'required': 'Last name is required.',
            },
            'email': {
                'required': 'Email is required.',
                'invalid': 'Enter a valid email address.'
            },
        }

    #first name validation 
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) < 3:
            raise forms.ValidationError("First name must be at least 3 characters.")

        if not first_name.replace(" ", "").isalpha():
            raise forms.ValidationError("First name must contain letters only.")

        return first_name.title()

   # last name validation
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if len(last_name) < 3:
            raise forms.ValidationError("Last name must be at least 3 characters.")

        if not last_name.replace(" ", "").isalpha():
            raise forms.ValidationError("Last name must contain letters only.")

        return last_name.title()

 # email validation
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if Staff.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already  used.")

        return email

# username validation
    def clean_username(self):
        username = self.cleaned_data.get('username').lower()

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters.")

        if " " in username:
            raise forms.ValidationError("Username must not contain spaces.")

        if Staff.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        return username

# login form logic
class StaffLoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        error_messages={
            'required': 'Username is required.'
        }
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        error_messages={
            'required': 'Password is required.'
        }
    )