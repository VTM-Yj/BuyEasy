import uuid
from django.test import TestCase, Client
from django.urls import reverse

from goods.models import Goods, Color, Size, Inventory, Category
from order.models import Order, OrderItem
from users.models import UserInfo
from address.models import Address
from cart.cartmanager import getCartManger


class OrderTests(TestCase):
    def setUp(self):
        """ Set up test user, address, cart, and product """
        self.client = Client()
        self.user = UserInfo.objects.create(user_name="testuser@example.com", pwd="password123")

        self.address = Address.objects.create(
            user_id=self.user.id,
            address_line1="123 Test Street",
            address_line2="Apt 4B",
            city="Test City",
            county="Test County",
            postcode="12345",
            phone="1234567890"
        )

        self.category = Category.objects.create(cname="Digital")
        # Create products
        self.product = Goods.objects.create(
            gname="Test Product",
            gDesc="Test Description",
            oldPrice=100.00,
            price=80.00,
            category=self.category
        )

        self.color = Color.objects.create(colorName="Red", colorUrl="red.png")
        self.size = Size.objects.create(sName="M")

        Inventory.objects.create(
            goods=self.product,
            color=self.color,
            size=self.size,
            count=10
        )

        self.client.session['user_id'] = self.user.id
        self.client.session.save()

    def test_create_order(self):
        """ Test creating an order from the cart """
        session = self.client.session
        session['user_id'] = self.user.id  # Make sure the user is logged in
        session.save()

        cart_manager = getCartManger(self.client)
        cart_manager.add(product_id=1, color_id=1, size_id=1, count=2)

        response = self.client.post(reverse('create_order'), {
            'selected_address_id': self.address.id,
            'stripe_token': 'tok_visa'
        })

        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user_id=self.user.id).first()
        self.assertIsNotNone(order, "Order was not created!")  # Ensure order creation is successful

    def test_order_detail(self):
        """ Test viewing an order's details """
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()  # Make sure the user is logged in

        order = Order.objects.create(
            order_number=uuid.uuid4(),
            user_id=self.user.id,
            total_amount=99.99,
            status="pending",
            shipping_address=self.address.address_line1
        )
        OrderItem.objects.create(
            order=order,
            product_id=1,
            product_name="Test Product",
            quantity=2,
            unit_price=49.99,
            subtotal=99.98
        )

        response = self.client.get(reverse('order_detail', args=[order.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(order.order_number))
        self.assertContains(response, "Test Product")

    def test_my_orders(self):
        """ Test viewing user's order list """
        order_uuid = uuid.uuid4()
        Order.objects.create(
            order_number=order_uuid,
            user_id=self.user.id,
            total_amount=50.00,
            status="paid",
            shipping_address=self.address.address_line1
        )

        # Make sure the user is logged in
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.get(reverse('my_orders'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(order_uuid))
