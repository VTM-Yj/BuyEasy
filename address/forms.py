# addresses/forms.py
from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'county', 'postcode', 'phone']
        widgets = {
            'address_line1': forms.TextInput(attrs={'placeholder': 'e.g. 10 Downing Street'}),
            'address_line2': forms.TextInput(attrs={'placeholder': 'e.g. Apt 2B (optional)'}),
            'city': forms.TextInput(attrs={'placeholder': 'e.g. London'}),
            'county': forms.TextInput(attrs={'placeholder': 'e.g. Greater London'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'e.g. SW1A 1AA'}),
            'phone': forms.TextInput(attrs={'placeholder': 'e.g. 01234 567890'}),
        }
