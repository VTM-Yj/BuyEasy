# orders/models.py
from django.db import models

class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True)  # 订单编号
    user_id = models.PositiveIntegerField()  # 购买用户
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # 总金额
    status = models.CharField(max_length=20, default="pending")  # 订单状态
    shipping_address = models.TextField()  # 收货地址
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # 关联订单
    product_id = models.PositiveIntegerField()  # 商品 ID
    product_name = models.CharField(max_length=255)  # 商品名称
    quantity = models.PositiveIntegerField()  # 购买数量
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # 单价
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # 小计

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
