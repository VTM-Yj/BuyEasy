from django.db import models
import  collections

# Create your models here.
class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return f'Category: {self.cname}'


class Goods(models.Model):
    gname = models.CharField(max_length=100)
    gDesc = models.CharField(max_length=100)
    oldPrice = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Goods: {self.gname}'

    def getImg(self):
        return self.inventory_set.first().color.colorUrl

    @property
    def getColorsList(self):
        colors = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colors:
                colors.append(color)
        return colors

    @property
    def getSizeList(self):
        sizesList = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizesList:
                sizesList.append(size)
        return sizesList

    @property
    def getDetailList(self):
        datas = collections.OrderedDict()

        for goodsDetail in self.goodsdetail_set.all():
            gDname = goodsDetail.name()
            if gDname not in datas:
                datas[gDname] = [goodsDetail.gdUrl]
            else:
                datas[gDname].append(goodsDetail.gdUrl)

        return datas


class GoodsDetailName(models.Model):
    gdName = models.CharField(max_length=30)

    def __str__(self):
        return f'GoodsDetailName: {self.gdName}'


class GoodsDetail(models.Model):
    gdUrl = models.ImageField(upload_to="")
    gdName = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def name(self):
        return self.gdName.gdName

class Size(models.Model):
    sName = models.CharField(max_length=10)

    def __str__(self):
        return f'Size: {self.sName}'


class Color(models.Model):
    colorName = models.CharField(max_length=10)
    colorUrl = models.ImageField(upload_to="color/")

    def __str__(self):
        return f'Color: {self.colorName}'


class Inventory(models.Model):
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
