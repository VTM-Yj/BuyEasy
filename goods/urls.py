from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:cid>/', views.IndexView.as_view(), name='category'),
    path('category/<int:cid>/page/<int:number>/', views.IndexView.as_view(), name='category_page'),
    path('goodsDetails/<int:gid>/', views.GoodsDetailsView.as_view(), name='goods_details'),
    path('search/', views.SearchView, name='search'),
]
