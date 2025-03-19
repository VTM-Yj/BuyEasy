# cart/tests.py
from django.test import TestCase
from collections import OrderedDict
from cart.models import CartItem
from cart.cartmanager import SessionCartManager, DBCartManager
from users.models import UserInfo
from goods.models import Goods, Color, Size, Category, Inventory
import jsonpickle  # Used to parse JSON data in the cart


class SessionCartManagerTest(TestCase):
    def setUp(self):
        """ Set up a simulated session environment """
        self.session = OrderedDict()  # Ensure key order
        self.cart_manager = SessionCartManager(self.session)

        # Create test data
        self.category = Category.objects.create(cname="Male")
        self.goods = Goods.objects.create(
            gname="Test Cart",
            gDesc="Test Description",
            oldPrice=100.00,
            price=80.00,
            category=self.category
        )
        self.color = Color.objects.create(colorName="Red", colorUrl="path/to/red.png")
        self.size = Size.objects.create(sName="M")
        Inventory.objects.create(count=10, color=self.color, goods=self.goods, size=self.size)

    def test_add_new_item(self):
        """ Test adding an item to the cart """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id
        count = 2

        self.cart_manager.add(str(product_id), str(color_id), str(size_id), count)
        key = f"{product_id},{color_id},{size_id}"

        # Ensure the item is added to the cart
        self.assertIn(key, self.session[self.cart_manager.cart_name])

        # Parse the stored JSON cart data
        cart_item = jsonpickle.decode(self.session[self.cart_manager.cart_name][key])
        self.assertEqual(cart_item.count, count)

    def test_update_item(self):
        """ Test updating the quantity of an item in the cart """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id
        initial_count = 2

        # Add an item first
        self.cart_manager.add(str(product_id), str(color_id), str(size_id), initial_count)

        # Update the item quantity
        self.cart_manager.update(str(product_id), str(color_id), str(size_id), step=1)

        key = f"{product_id},{color_id},{size_id}"

        # Parse the stored JSON data
        cart_item = jsonpickle.decode(self.session[self.cart_manager.cart_name][key])

        self.assertEqual(cart_item.count, initial_count + 1)

    def test_delete_item(self):
        """ Test deleting an item from the cart """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id
        count = 2

        self.cart_manager.add(str(product_id), str(color_id), str(size_id), count)
        key = f"{product_id},{color_id},{size_id}"

        self.assertIn(key, self.session[self.cart_manager.cart_name])
        self.cart_manager.delete(str(product_id), str(color_id), str(size_id))

        self.assertNotIn(key, self.session[self.cart_manager.cart_name])

    def test_query_all(self):
        """ Test retrieving all cart items """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id

        # Add the same item twice to ensure the quantity is merged
        self.cart_manager.add(str(product_id), str(color_id), str(size_id), 2)
        self.cart_manager.add(str(product_id), str(color_id), str(size_id), 3)

        # Parse the JSON data returned by queryAll()
        cart_items = [jsonpickle.decode(item) for item in self.cart_manager.queryAll()]

        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0].count, 5)


class DBCartManagerTest(TestCase):
    def setUp(self):
        """ Set up test data for database-based cart management """
        self.user = UserInfo.objects.create(user_name="testuser", pwd="password")
        self.user.refresh_from_db()  # Ensure database synchronization

        # Instantiate DBCartManager directly
        self.cart_manager = DBCartManager(self.user)

        # Create test data
        self.category = Category.objects.create(cname="Male")
        self.goods = Goods.objects.create(
            gname="Test Product",
            gDesc="Test Description",
            oldPrice=100.00,
            price=80.00,
            category=self.category
        )
        self.color = Color.objects.create(colorName="Blue", colorUrl="path/to/blue.png")
        self.size = Size.objects.create(sName="L")
        Inventory.objects.create(count=10, color=self.color, goods=self.goods, size=self.size)

    def test_db_add_new_item(self):
        """ Test adding a new item to the database-based cart """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id
        count = 2

        self.cart_manager.add(str(product_id), str(color_id), str(size_id), count)

        # Ensure the item exists in the database
        cart_items = CartItem.objects.filter(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id,
            user=self.user
        )

        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.first().count, count)

    def test_db_update_item(self):
        """ Test updating the quantity of an item in the database-based cart """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id
        initial_count = 2

        # Add an item first
        self.cart_manager.add(str(product_id), str(color_id), str(size_id), initial_count)

        # Update the item quantity
        self.cart_manager.update(str(product_id), str(color_id), str(size_id), step=1)

        cart_item = CartItem.objects.get(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id,
            user=self.user
        )

        self.assertEqual(cart_item.count, initial_count + 1)

    def test_db_delete_item(self):
        """ Test deleting an item from the database-based cart """
        product_id = self.goods.id
        color_id = self.color.id
        size_id = self.size.id
        count = 2

        self.cart_manager.add(str(product_id), str(color_id), str(size_id), count)
        self.cart_manager.delete(str(product_id), str(color_id), str(size_id))

        cart_items = CartItem.objects.filter(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id,
            user=self.user,
            is_deleted=False
        )

        self.assertEqual(cart_items.count(), 0)
