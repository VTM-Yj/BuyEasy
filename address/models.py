# addresses/models.py
from django.db import models
from django.core.validators import RegexValidator

# Define a simple UK postcode validator
postcode_validator = RegexValidator(
    regex=r'^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$',
    message="Please enter a valid UK postcode, e.g. 'SW1A 1AA'."
)

class Address(models.Model):
    # Assume the user is represented by a foreign key to your custom user model or simply store user_id as integer.
    # Here we store user_id as integer.
    user_id = models.PositiveIntegerField()
    address_line1 = models.CharField(max_length=100, help_text="Street address and number")
    address_line2 = models.CharField(max_length=100, blank=True, null=True, help_text="Apartment or unit (optional)")
    city = models.CharField(max_length=50, help_text="City")
    county = models.CharField(max_length=50, help_text="County or region")
    postcode = models.CharField(max_length=10, validators=[postcode_validator], help_text="Postcode")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_line1}, {self.city} ({self.postcode})"
