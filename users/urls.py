from django.urls import path
from . import views
from .views import CheckUserNameView

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('checkUserName/', views.CheckUserNameView.as_view(), name='checkUserName'),
    path('center/', views.UserCenterView.as_view(), name='center'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('loadCode/', views.LoadCodeView.as_view(), name='loadCode'),
    path('checkCode/', views.CheckCodeView.as_view(), name='checkCode'),


]
