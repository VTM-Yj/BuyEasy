# orders/forms.py
from django import forms


class OrderForm(forms.Form):
    # 如果用户选择已有地址，则该字段存放地址ID
    selected_address_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    # 新地址字段，如果用户没有选择已有地址，则需要填写新地址
    new_address_line1 = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'Street address and number'}))
    new_address_line2 = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'Apartment or unit (optional)'}))
    new_city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    new_county = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'County or region'}))
    new_postcode = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Postcode'}))
    new_phone = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Phone number (optional)'}))
