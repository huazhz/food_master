import os
import json
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators import csrf
from django.core.paginator import Paginator
from front.models import Recipe, RecipeIngredient, RecipeCategory
from utils import common_utils
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from front.serializers import RecipeSerializer


# Create your views here.
# I know, shut your mouth.

@cache_page(15)
def index(req):
    """ 首页 """
    recipe1 = Recipe.objects.filter(category__name='家常菜') \
                  .exclude(rate_score='暂无') \
                  .exclude(cover_img='暂无') \
                  .order_by('-rate_score')[:10]
    recipe2 = Recipe.objects.filter(category__name='快手菜') \
                  .exclude(rate_score='暂无') \
                  .exclude(cover_img='暂无') \
                  .order_by('-rate_score')[:10]
    recipe3 = Recipe.objects.filter(category__name='下饭菜') \
                  .exclude(rate_score='暂无') \
                  .exclude(cover_img='暂无') \
                  .order_by('-rate_score')[:10]
    
    return render(req, 'front/index.html', locals())


@cache_page(60 * 15)
def category(req, id, page_num=1):
    """ 分类列表 """
    obj_list1 = Recipe.objects.filter(category__id=id) \
                    .order_by('-rate_score')[:30]
    obj_list2 = Recipe.objects.filter(category__id=id) \
                    .order_by('-add_time')[:30]
    obj_list3 = Recipe.objects.filter(category__id=id) \
                    .order_by('-name')[:30]
    cat = RecipeCategory.objects.get(id=id)
    cat_list = RecipeCategory.objects.all()[:30]
    paginator = Paginator(obj_list3, 10)
    result = paginator.get_page(page_num)
    page_nearby_range = common_utils.get_nearby_pages(result)
    return render(req, 'front/category.html',
                  context={'result': result, 'key': id, 'cat': cat, 'cat_list': cat_list,
                           'obj_list1': obj_list1,
                           'obj_list2': obj_list2,
                           'obj_list3': obj_list3,
                           'page_nearby_range': page_nearby_range})


@cache_page(60)
def search_result(req, key, page_num=1):
    """ 搜索列表展示页"""
    obj_list = Recipe.objects.filter(name__contains=key) \
        .order_by('-rate_score')
    paginator = Paginator(obj_list, 10)
    result = paginator.get_page(page_num)
    page_nearby_range = common_utils.get_nearby_pages(result)
    return render(req, 'front/list.html', context={'result': result, 'key': key,
                                                   'page_nearby_range': page_nearby_range})


@cache_page(60 * 15)
def recipe_details(req, id=None):
    if not id:
        return Http404('')
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        raise Http404('s')
    category = recipe.category.all()
    recipe_ingredient = RecipeIngredient.objects.filter(recipe__id=id)
    first_cate = category[0] if category else None
    recipe_steps = recipe.recipestep_set.all()
    return render(req, 'front/recipe.html', locals())


def sitemap(req):
    # with open('./templates/front/sitemap.txt') as f:
    #     return HttpResponse(f.readlines())
    return render(req, 'front/sitemap.txt')


@csrf.csrf_exempt
def webhook(req):
    """ 利用github的 webhook功能实现自动部署更新 """
    print('webhook is running!')
    
    msg = os.popen('sh /home/www/food_master/webhook.sh').read()
    data = {'status': 'ok', 'message': msg}
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def recipe_list(request):
    """ list first 10 recipes """
    if request.method == "GET":
        recipes = Recipe.objects.all()[:10]
        recipe_serializer = RecipeSerializer(recipes, many=True)
        return JsonResponse(recipe_serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def recipe_detail(request, id):
    """ Retrieve, update or delete a recipe. """
    try:
        recipe = Recipe.objects.get(pk=id)
    except Recipe.DoesNotExist:
        return HttpResponse(404)
    
    if request.method == "GET":
        serializer = RecipeSerializer(recipe)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RecipeSerializer(recipe, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        recipe.delete()
        return HttpResponse(status=204)
