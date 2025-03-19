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
                    "error": "Please select an address。"
                })

            cart_manager = getCartManger(request)
            cart_items = cart_manager.queryAll()
            if not cart_items:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "Cart is empty"
                })

            total_amount = sum(item.getSubTotal() for item in cart_items)

            stripe_token = request.POST.get("stripe_token")
            if not stripe_token:
                return render(request, "order_form.html", {
                    "form": form,
                    "addresses": user_addresses,
                    "error": "Please re-try。"
                })

            try:
                with transaction.atomic():
                    # Create an order, the order number will automatically increase
                    order = Order.objects.create(
                        user_id=user_id,
                        total_amount=total_amount,
                        status="pending",
                        shipping_address=str(address)
                    )

                    # Create a line item
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product_id=item.product_id,
                            product_name=item.getGoods().gDesc,
                            quantity=item.count,
                            unit_price=item.getGoods().price,
                            subtotal=item.getSubTotal()
                        )

                    # Empty Cart
                    cart_manager.clear()

                    # Make a Stripe payment
                    charge = stripe.Charge.create(
                        amount=int(order.total_amount * 100),
                        currency="usd",
                        source=stripe_token,
                        description=f"Order {order.order_number}"
                    )

                    # Update order status
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


def my_orders(request):
    # Get the current user's ID
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("/users/login/")

    # Query all orders of the current user, sorted in descending order by creation time
    orders = Order.objects.filter(user_id=user_id).order_by("-created_at")

    return render(request, "my_orders.html", {"orders": orders})
