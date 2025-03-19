from urllib.request import HTTPRedirectHandler

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from order.models import Order
from users.models import UserInfo
from utils.code import *


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user_name = request.POST.get('user_name', '')
        pwd = request.POST.get('pwd', '')

        user = UserInfo.objects.create(user_name=user_name, pwd=pwd)

        if user:
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('center'))

        return HttpResponseRedirect(reverse('register'))


class CheckUserNameView(View):
    def get(self, request):
        user_name = request.GET.get('user_name', '')
        user_list = UserInfo.objects.filter(user_name=user_name)

        flag = False

        if user_list:
            flag = True
        return JsonResponse({'flag': flag})


class UserCenterView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('login'))
        try:
            user = UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            return HttpResponseRedirect(reverse('login'))

        pending_orders = Order.objects.filter(user_id=user_id, status='paid')
        pending_orders_count = pending_orders.count()

        return render(request, 'center.html', {'current_user': user, 'pending_orders_count': pending_orders_count})


class LogoutView(View):
    def post(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']

        return JsonResponse({'del_flag': True})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_name = request.POST.get('user_name', '')
        pwd = request.POST.get('pwd', '')

        try:
            user = UserInfo.objects.get(user_name=user_name)
        except UserInfo.DoesNotExist:
            user = None

        if user and user.pwd == pwd:
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('center'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})


class LoadCodeView(View):
    def get(self, request):
        img, code_str = gene_code()
        request.session['code_str'] = code_str
        return HttpResponse(img, content_type='image/png')


class CheckCodeView(View):
    def get(self, request):
        code = request.GET.get('code', '')
        session_code = request.session.get('code_str', None)
        flag = (code == session_code)
        return JsonResponse({'checkFlag': flag})

