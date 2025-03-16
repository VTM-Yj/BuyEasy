# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("myorders/", views.my_orders, name="my_orders"),
    path('create/', views.create_order, name='create_order'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
