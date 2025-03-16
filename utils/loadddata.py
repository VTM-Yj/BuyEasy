from django.db.transaction import atomic
import json
from goods.models import *


@atomic
def test_model():
    with open('utils/shop.json') as fr:
        datas = json.load(fr)

    for data in datas:
        cate = Category.objects.create(cname=data['category'])

        _goods = data['goods']

        for good_data in _goods:
            good = Goods.objects.create(
                gname=good_data['goodsname'],
                gDesc=good_data['goods_desc'],
                price=good_data['goods_price'],
                oldPrice=good_data['goods_oldprice'],
                category=cate
            )


            sizes = []
            for _size in good_data.get('sizes', []):
                size_name = _size[0]
                size, created = Size.objects.get_or_create(sName=size_name)
                sizes.append(size)


            colors = []
            for _color in good_data.get('colors', []):
                color = Color.objects.create(colorName=_color[0], colorUrl=_color[1])
                colors.append(color)


            for _spec in good_data.get('specs', []):
                goods_detail_name, created = GoodsDetailName.objects.get_or_create(gdName=_spec[0])
                for img in _spec[1]:
                    GoodsDetail.objects.create(goods=good, gdName=goods_detail_name, gdUrl=img)


            for c in colors:
                for s in sizes:
                    Inventory.objects.create(count=100,goods=good, color=c, size=s)


def deleteall():
    Category.objects.filter().delete()
    Color.objects.filter().delete()
    Size.objects.filter().delete()