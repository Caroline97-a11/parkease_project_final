from django import forms
from payment.models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = '__all__'

        widgets = {
            "Payment_method": forms.Select(attrs={
                "class": "form-select"
            })
        }

        error_messages = {
            "Payment_method": {
                "required": "Please select a payment method."
            }
        }

   # validating the payment method 
    def clean_Payment_method(self):
        method = self.cleaned_data.get("Payment_method")

        if not method:
            raise forms.ValidationError("Payment method is required.")