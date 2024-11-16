from django import forms

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15)

class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=6)