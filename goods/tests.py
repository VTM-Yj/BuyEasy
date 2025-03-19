from django.test import TestCase
from goods.models import Goods, Category

class GoodsModelTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(cname="Male")
        Goods.objects.create(
            gname="Casual shirt",
            gDesc="ARKET Mens Long-sleeved Linen Casual Shirt Dark Blue Shirt 2025 Summer Classic 1034463002",
            oldPrice=100.00,
            price=80.00,
            category=cat
        )

    def test_goods_str(self):
        goods = Goods.objects.get(gname="Casual shirt")
        self.assertEqual(str(goods), "Goods: Casual shirt")
