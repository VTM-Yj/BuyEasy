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
                    "error": "未选择地址，请添加或选择一个地址。"
                })

            cart_manager = getCartManger(request)
            cart_items = cart_manager.queryAll()
            if not cart_items:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "购物车为空，无法下单。"
                })

            total_amount = sum(item.getSubTotal() for item in cart_items)

            stripe_token = request.POST.get("stripe_token")
            if not stripe_token:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "支付信息错误，请重试。"
                })

            try:
                with transaction.atomic():
                    # 创建订单，订单号自动递增
                    order = Order.objects.create(
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

                    # 进行 Stripe 支付
                    charge = stripe.Charge.create(
                        amount=int(order.total_amount * 100),
                        currency="usd",
                        source=stripe_token,
                        description=f"Order {order.order_number}"
                    )

                    # 更新订单状态
                    order.status = "paid"
                    order.save()

                return HttpResponseRedirect(reverse("order_detail", args=[order.id]))
            except Exception as e:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": f"支付失败: {e}"
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


def my_orders(request):
    # 获取当前用户的ID（假设保存在 session 中）
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("/users/login/")

    # 查询当前用户的所有订单，按创建时间倒序排列
    orders = Order.objects.filter(user_id=user_id).order_by("-created_at")

    return render(request, "my_orders.html", {"orders": orders})
