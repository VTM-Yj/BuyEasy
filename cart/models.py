import math

from django.db import models

from goods.models import Goods, Color, Size
from users.models import UserInfo


# Create your models here.

class CartItem(models.Model):
    product_id = models.PositiveIntegerField()
    color_id = models.PositiveIntegerField()
    size_id = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('product_id', 'color_id', 'size_id'),)

    def getGoods(self):
        return Goods.objects.get(id=self.product_id)

    def getColor(self):
        return Color.objects.get(id=self.color_id)

    def getSize(self):
        return Size.objects.get(id=self.size_id)

    def getSubTotal(self):
        return float(self.getGoods().price) * int(self.count)
