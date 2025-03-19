from django.test import TestCase, Client
from django.urls import reverse
from goods.models import Category, Goods, GoodsDetailName, GoodsDetail, Size, Color, Inventory


class GoodsTests(TestCase):
    def setUp(self):
        """ Set up test categories, products, colors, sizes, and inventory """
        self.client = Client()

        #  Creat category
        self.category = Category.objects.create(cname="Digital")

        #  Creat goods
        self.goods = Goods.objects.create(
            gname="Test Laptop",
            gDesc="High-performance laptop",
            oldPrice=120.00,
            price=99.00,
            category=self.category
        )

        # Creat color
        self.color = Color.objects.create(colorName="Black", colorUrl="black.png")

        # Creat size
        self.size = Size.objects.create(sName="15-inch")

        # Creat inventory
        self.inventory = Inventory.objects.create(
            count=10,
            color=self.color,
            goods=self.goods,
            size=self.size
        )

        # Creat detail_name
        self.detail_name = GoodsDetailName.objects.create(gdName="Product Image")

        # Creat goods_detail
        self.goods_detail = GoodsDetail.objects.create(
            gdUrl="laptop_image.png",
            gdName=self.detail_name,
            goods=self.goods
        )

    def test_category_creation(self):
        """ Test category creation """
        self.assertEqual(self.category.cname, "Digital")
        self.assertEqual(str(self.category), "Category: Digital")

    def test_goods_creation(self):
        """ Test goods creation """
        self.assertEqual(self.goods.gname, "Test Laptop")
        self.assertEqual(float(self.goods.price), 99.00)
        self.assertEqual(str(self.goods), "Goods: Test Laptop")

    def test_goods_image(self):
        """ Test getImg method for goods """
        self.assertEqual(self.goods.getImg(), "black.png")  # Should return the first color image

    def test_goods_colors_list(self):
        """ Test getColorsList method for goods """
        colors = self.goods.getColorsList
        self.assertEqual(len(colors), 1)
        self.assertEqual(colors[0].colorName, "Black")

    def test_goods_sizes_list(self):
        """ Test getSizeList method for goods """
        sizes = self.goods.getSizeList
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].sName, "15-inch")

    def test_goods_detail_list(self):
        """ Test getDetailList method for goods """
        details = self.goods.getDetailList
        self.assertIn("Product Image", details)
        self.assertIn("laptop_image.png", details["Product Image"])

    def test_goods_detail_name(self):
        """ Test goods detail name """
        self.assertEqual(str(self.detail_name), "GoodsDetailName: Product Image")

    def test_index_view(self):
        """ Test the homepage loads correctly """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BuyEasy")

    def test_category_view(self):
        """ Test category page loads correctly """
        response = self.client.get(reverse('category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.cname)

    def test_goods_detail_view(self):
        """ Test goods detail page loads correctly """
        response = self.client.get(reverse('goods_details', args=[self.goods.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.goods.gname)
        self.assertContains(response, self.goods.price)

    def test_search_view(self):
        """ Test search functionality """
        response = self.client.get(reverse('search') + "?q=Laptop")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Laptop")
