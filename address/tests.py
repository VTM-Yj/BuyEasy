# addresses/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from address.models import Address

class AddressModelTest(TestCase):
    def setUp(self):
        # Create a valid Address instance
        self.address = Address.objects.create(
            user_id=1,
            address_line1="10 Downing Street",
            address_line2="",
            city="London",
            county="Greater London",
            postcode="SW1A 2AA",
            phone="01234567890"
        )

    def test_address_str(self):
        """
        Test that the __str__ method of the Address model returns a correct string
        """
        expected_str = "10 Downing Street, London (SW1A 2AA)"
        self.assertEqual(str(self.address), expected_str)

    def test_postcode_validation(self):
        """
        Tests whether a ValidationError is thrown when the postal code format is incorrect
        """
        # Create an address instance with a postcode that does not conform to the UK format
        invalid_address = Address(
            user_id=1,
            address_line1="123 Fake Street",
            city="London",
            county="Greater London",
            postcode="INVALID",  # Invalid postal code
            phone="01234567890"
        )
        # Call the full_clean method to perform model validation
        with self.assertRaises(ValidationError):
            invalid_address.full_clean()  # full_clean() performs field validation

    def test_address_creation(self):
        """
        Test whether the data can be saved normally when creating an address
        """
        addr = Address.objects.create(
            user_id=2,
            address_line1="221B Baker Street",
            address_line2="",
            city="London",
            county="Greater London",
            postcode="NW1 6XE",
            phone="0987654321"
        )
        self.assertIsNotNone(addr.id)
        self.assertEqual(addr.city, "London")
