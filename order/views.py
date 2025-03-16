# orders/views.py
import uuid
import stripe
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from .models import Order, OrderItem
from .forms import OrderForm
from cart.cartmanager import getCartManger
from address.models import Address

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_order(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("/users/login/")

    # 获取用户地址
    user_addresses = Address.objects.filter(user_id=user_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            selected_address_id = form.cleaned_data.get('selected_address_id')
            if selected_address_id:
                address = get_object_or_404(Address, pk=selected_address_id, user_id=user_id)
            else:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "No address selected. Please add or select an address."
                })

            # 获取购物车数据
            cart_manager = getCartManger(request)
            cart_items = cart_manager.queryAll()

            if not cart_items:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "Your cart is empty."
                })

            total_amount = sum(item.getSubTotal() for item in cart_items)

            # 获取 Stripe Token
            stripe_token = request.POST.get("stripe_token")
            if not stripe_token:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "Stripe token missing. Please try again."
                })

            try:
                with transaction.atomic():
                    # 创建订单
                    order = Order.objects.create(
                        order_number=str(uuid.uuid4()),
                        user_id=user_id,
                        total_amount=total_amount,
                        status="pending",
                        shipping_address=str(address)
                    )

                    # 创建订单项
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product_id=item.product_id,
                            product_name=item.getGoods().gDesc,
                            quantity=item.count,
                            unit_price=item.getGoods().price,
                            subtotal=item.getSubTotal()
                        )

                    # 清空购物车
                    cart_manager.clear()

                    # Stripe 收款
                    charge = stripe.Charge.create(
                        amount=int(order.total_amount * 100),  # 分为单位
                        currency="usd",
                        source=stripe_token,
                        description=f"Order {order.order_number}"
                    )
                    # 如果成功，则订单状态更新
                    order.status = "paid"
                    order.save()

                return HttpResponseRedirect(reverse("order_detail", args=[order.id]))
            except Exception as e:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": f"Payment failed: {e}"
                })

    else:
        form = OrderForm()

    return render(request, "order_form.html", {
        "form": form,
        "addresses": user_addresses,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY
    })


def order_detail(request, order_id):
    user_id = request.session.get('user_id')
    order = get_object_or_404(Order, id=order_id, user_id=user_id)
    return render(request, "order_detail.html", {"order": order})


# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from django.urls import reverse


def my_orders(request):
    # 获取当前用户的ID（假设保存在 session 中）
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("/users/login/")

    # 查询当前用户的所有订单，按创建时间倒序排列
    orders = Order.objects.filter(user_id=user_id).order_by("-created_at")

    return render(request, "my_orders.html", {"orders": orders})
