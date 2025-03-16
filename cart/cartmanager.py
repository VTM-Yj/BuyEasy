from collections import OrderedDict

from users.models import UserInfo
from .models import CartItem
from django.db.models import F
import jsonpickle


class CartManager(object):
    def add(self, product_id, color_id, size_id, count, *args, **kwargs):
        pass

    def delete(self, product_id, color_id, size_id, *args, **kwargs):
        pass

    def update(self, product_id, color_id, size_id, count, step, *args, **kwargs):
        pass

    def queryAll(self, *args, **kwargs):
        pass


# 当前用户未登录时使用 Session 管理购物车
class SessionCartManager(CartManager):
    cart_name = 'cart'

    def __init__(self, session):
        self.session = session
        # 如果购物车不存在则创建
        if self.cart_name not in self.session:
            self.session[self.cart_name] = OrderedDict()

    def __get_key(self, product_id, color_id, size_id):
        # 使用 f-string 拼接参数，确保唯一性
        return f"{product_id},{color_id},{size_id}"

    def add(self, product_id, color_id, size_id, count, *args, **kwargs):
        key = self.__get_key(product_id, color_id, size_id)
        if key in self.session[self.cart_name]:
            self.update(product_id, color_id, size_id, count, *args, **kwargs)
        else:
            cart_item = CartItem(
                product_id=product_id,
                color_id=color_id,
                size_id=size_id,
                count=count
            )
            self.session[self.cart_name][key] = jsonpickle.encode(cart_item)

    def delete(self, product_id, color_id, size_id, *args, **kwargs):
        key = self.__get_key(product_id, color_id, size_id)
        if key in self.session[self.cart_name]:
            del self.session[self.cart_name][key]
            self.session.modified = True

    def update(self, product_id, color_id, size_id, step, *args, **kwargs):
        key = self.__get_key(product_id, color_id, size_id)
        if key in self.session[self.cart_name]:
            cartitem = self.session[self.cart_name][key]
            cartitem['count'] = int(cartitem['count']) + int(step)
        else:
            raise Exception('SessionCartManager update error: key not found')

    def queryAll(self, *args, **kwargs):
        # 返回购物车中所有项的字典列表
        return list(self.session[self.cart_name].values())

    def migrateSession2DB(self):
        # 注意：这里假设 session 中的 'user' 存储的是用户对象（或用户ID），具体需要根据项目实际调整
        if 'user' in self.session:
            user = self.session.get('user')
            for cartitem in self.queryAll():
                # 检查数据库中是否已有该购物项
                if CartItem.objects.filter(
                        product_id=cartitem['product_id'],
                        color_id=cartitem['color_id'],
                        size_id=cartitem['size_id']
                ).count() == 0:
                    CartItem.objects.create(
                        product_id=cartitem['product_id'],
                        color_id=cartitem['color_id'],
                        size_id=cartitem['size_id'],
                        count=cartitem['count'],
                        user=user
                    )
                else:
                    item = CartItem.objects.get(
                        product_id=cartitem['product_id'],
                        color_id=cartitem['color_id'],
                        size_id=cartitem['size_id']
                    )
                    item.count = int(item.count) + int(cartitem['count'])
                    item.save()
            del self.session[self.cart_name]


# 用户已登录时使用数据库管理购物车
class DBCartManager(CartManager):
    def __init__(self, user):
        self.user = user

    def add(self, product_id, color_id, size_id, count, *args, **kwargs):
        if self.user.cartitem_set.filter(
                product_id=product_id,
                color_id=color_id,
                size_id=size_id
        ).exists():
            self.update(product_id, color_id, size_id, count, *args, **kwargs)
        else:
            CartItem.objects.create(
                product_id=product_id,
                color_id=color_id,
                size_id=size_id,
                count=count,
                user=self.user
            )

    def delete(self, product_id, color_id, size_id, *args, **kwargs):
        self.user.cartitem_set.filter(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id
        ).update(count=0, is_deleted=True)

    def update(self, product_id, color_id, size_id, step, *args, **kwargs):
        self.user.cartitem_set.filter(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id
        ).update(count=F('count') + int(step), is_deleted=False)

    def queryAll(self, *args, **kwargs):
        return self.user.cartitem_set.order_by('id').filter(is_deleted=False).all()

    def get_cartitems(self, product_id, size_id, color_id, *args, **kwargs):
        return self.user.cartitem_set.get(
            product_id=product_id,
            size_id=size_id,
            color_id=color_id
        )

    def clear(self):
        self.user.cartitem_set.all().delete()




# 工厂方法：根据当前用户是否登录返回相应的 CartManager 对象
def getCartManger(request):
    if request.session.get('user_id'):
        user = UserInfo.objects.get(pk=request.session.get('user_id'))
        return DBCartManager(user)
    return SessionCartManager(request.session)
