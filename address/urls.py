# addresses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.address_list, name='address_list'),
    path('add/', views.address_add, name='address_add'),
    path('edit/<int:pk>/', views.address_edit, name='address_edit'),
    path('delete/<int:pk>/', views.address_delete, name='address_delete'),
]
