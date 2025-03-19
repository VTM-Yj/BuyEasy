# orders/forms.py
from django import forms


class OrderForm(forms.Form):
    # If the user selects an existing address, this field stores the address ID
    selected_address_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    # New address field, if the user does not select an existing address, then the new address needs to be filled in
    new_address_line1 = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'Street address and number'}))
    new_address_line2 = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'Apartment or unit (optional)'}))
    new_city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    new_county = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'County or region'}))
    new_postcode = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Postcode'}))
    new_phone = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Phone number (optional)'}))
