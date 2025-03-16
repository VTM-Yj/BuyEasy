from http.client import responses

from django.shortcuts import render
from django.views import View

from goods.models import *
from django.core.paginator import Paginator
import math


# Create your views here.

class IndexView(View):
    def get(self, request, cid=2, number=1):

        cid = int(cid)

        number = int(number)

        categoryList = Category.objects.all().order_by('id')

        goodsList = Goods.objects.filter(category_id=cid).order_by('id')

        pager = Paginator(goodsList, 8)

        page_goodsList = pager.page(number)

        begin = (number - int(math.ceil(10.0 / 2)))
        if begin < 1:
            begin = 1

        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages

        if end < 10:
            begin = 1

        else:
            begin = end - 9

        pageList = range(begin, end + 1)

        return render(request, 'index.html',
                      {'categoryList': categoryList, 'goodsList': page_goodsList, 'currentCid': cid,
                       'pageList': pageList, 'currentNumber': number})


def recommendView(func):
    def wrapper(self, request, gid, *args, **kwargs):
        # 从 cookie 中获取推荐商品的ID字符串，多个ID用空格分隔
        cookie_str = request.COOKIES.get('recommend', '')
        goodsIdList = [token for token in cookie_str.split() if token.strip()]


        # 获取当前商品对象，避免重复查询
        current_goods = Goods.objects.get(id=gid)

        # 构造推荐列表：排除当前商品，同时要求同一类别；最多取前4个
        recommendObjList = [
                               Goods.objects.get(id=gsId)
                               for gsId in goodsIdList
                               if
                               gsId != str(gid) and Goods.objects.get(id=gsId).category_id == current_goods.category_id
                           ][:4]

        # 调用原函数，将推荐列表传入
        response = func(self, request, gid, recommendObjList, *args, **kwargs)

        # 更新 goodsIdList，将当前商品ID移到最前面
        str_gid = str(gid)
        if str_gid in goodsIdList:
            goodsIdList.remove(str_gid)
            goodsIdList.insert(0, str_gid)
        else:
            goodsIdList.insert(0, str_gid)

        # 更新 cookie：将ID列表以空格分隔保存
        response.set_cookie('recommend', ' '.join(goodsIdList), max_age=3 * 24 * 3600)
        return response

    return wrapper


class GoodsDetailsView(View):
    @recommendView
    def get(self, request, gid, recommendList=[]):
        goods_id = int(gid)
        goods = Goods.objects.get(id=goods_id)
        return render(request, 'detail.html', {'goods': goods, 'recommendList': recommendList})
