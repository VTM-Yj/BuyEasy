from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .cartmanager import *

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .cartmanager import getCartManger


class AddCartView(View):
    def post(self, request):
        flag = request.POST.get('flag', '')
        data = request.POST.dict()
        print(data)
        # 如果前端传过来 goods_id，则转换为 product_id
        if 'goods_id' in data:
            data['product_id'] = data.pop('goods_id')
        cartManagerObj = getCartManger(request)
        if flag == 'add':
            cartManagerObj.add(**data)
        elif flag == 'plus':
            # 对于加操作，将 step 设置为 1
            cartManagerObj.update(step=1, **data)
        elif flag == 'minus':
            # 对于减操作，将 step 设置为 -1
            cartManagerObj.update(step=-1, **data)
        elif flag == 'delete':
            cartManagerObj.delete(**data)
        return HttpResponseRedirect(reverse('queryAll'))


class QueryAllView(View):
    def get(self, request):
        cartManagerObj = getCartManger(request)
        cartList = cartManagerObj.queryAll()
        return render(request, 'cart.html', {'cartList': cartList})
