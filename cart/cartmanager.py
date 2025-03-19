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


# Use Session to manage the cart when the user is not logged in
class SessionCartManager(CartManager):
    cart_name = 'cart'

    def __init__(self, session):
        self.session = session
        # Create a cart if it does not exist
        if self.cart_name not in self.session:
            self.session[self.cart_name] = OrderedDict()

    def __get_key(self, product_id, color_id, size_id):
        # Use f-string to concatenate parameters to ensure uniqueness
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
            # Decode JSON first
            cartitem = jsonpickle.decode(self.session[self.cart_name][key])

            # Update the quantity
            cartitem.count = int(cartitem.count) + int(step)

            # Re-encode and save back to session
            self.session[self.cart_name][key] = jsonpickle.encode(cartitem)
        else:
            raise Exception('SessionCartManager update error: key not found')

    def queryAll(self, *args, **kwargs):
        # Return a list of all cart items
        return list(self.session[self.cart_name].values())

    def migrateSession2DB(self):
        if 'user' in self.session:
            user = self.session.get('user')
            for cartitem in self.queryAll():
                existing_item = CartItem.objects.filter(
                    product_id=cartitem['product_id'],
                    color_id=cartitem['color_id'],
                    size_id=cartitem['size_id'],
                    user=user
                ).first()

                if existing_item:
                    # ✅ 避免重复：更新数量，而不是新建
                    existing_item.count += int(cartitem['count'])
                    existing_item.is_deleted = False  # 重新激活删除的商品
                    existing_item.save()
                else:
                    # ✅ 只有当数据库中 **没有此商品** 时才新建
                    CartItem.objects.create(
                        product_id=cartitem['product_id'],
                        color_id=cartitem['color_id'],
                        size_id=cartitem['size_id'],
                        count=cartitem['count'],
                        user=user
                    )

            # ✅ 清空 session 购物车，防止重复迁移
            self.session.pop(self.cart_name, None)
            self.session.modified = True


# Use Database to manage the cart when the user is logged in
class DBCartManager(CartManager):
    def __init__(self, user):
        self.user = user

    def add(self, product_id, color_id, size_id, count, *args, **kwargs):
        cart_item = self.user.cartitem_set.filter(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id
        ).first()

        if cart_item:
            # If the item exists, update the quantity
            if cart_item.is_deleted:
                cart_item.is_deleted = False
                cart_item.count = int(count)  # Reset quantity
            else:
                cart_item.count += int(count)
            cart_item.save()
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


# Factory Method: Returns the appropriate CartManager object based on the user's login status
def getCartManger(request):
    if request.session.get('user_id'):
        user = UserInfo.objects.get(pk=request.session.get('user_id'))
        return DBCartManager(user)
    return SessionCartManager(request.session)
