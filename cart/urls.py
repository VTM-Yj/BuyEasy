from django.urls import path
from . import views

urlpatterns = [
    path('addCart/', views.AddCartView.as_view(), name='addCart'),
    path('queryAll/', views.QueryAllView.as_view(), name='queryAll'),
]
