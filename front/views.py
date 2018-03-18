import os
import json
import logging
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from front.models import Recipe, RecipeIngredient, RecipeCategory, MemberRecipeList
from utils import common_utils
from front import rs
from django.views.decorators.cache import cache_page

from django.core.cache import cache

logger = logging.getLogger("default")
logger.info("This is an error msg")


# Create your views here.
# I know, shut your mouth.

@cache_page(15)
def index(req):
    """ 首页 """
    
    logger.info('fuck you!')
    
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


def menu(req):
    categories = RecipeCategory.objects.all()[:100]
    
    return render(req, 'front/menu.html', locals())


def recipe_list(req, id, page=1):
    list_obj = MemberRecipeList.objects.get(id=id)
    list_name = list_obj.name
    recipes = list_obj.recipes.all()
    print(recipes.all())
    return render(req, 'front/recipe_list.html',
                  context={'recipes': recipes, 'list_name': list_name, })


@cache_page(60 * 15)
def category_detail(req, id, page_num=1):
    """ 分类列表 """
    
    menu_name = RecipeCategory.objects.get(id=id).name
    
    similar_menus = MemberRecipeList.objects.filter(name__contains=menu_name)[:20]
    
    obj_list1 = Recipe.objects.filter(category__id=id) \
        .order_by('-rate_score')
    obj_list2 = Recipe.objects.filter(category__id=id) \
        .order_by('-add_time')
    obj_list3 = Recipe.objects.filter(category__id=id) \
        .order_by('-name')
    cat = RecipeCategory.objects.get(id=id)
    cat_list = RecipeCategory.objects.all()[:30]
    paginator1 = Paginator(obj_list1, 20)
    paginator2 = Paginator(obj_list2, 20)
    paginator3 = Paginator(obj_list3, 20)
    result1 = paginator1.get_page(page_num)
    result2 = paginator2.get_page(page_num)
    result3 = paginator3.get_page(page_num)
    page_nearby_range = common_utils.get_nearby_pages(result1)
    return render(req, 'front/category_detail.html',
                  context={
                      'result1': result1,
                      'result2': result2,
                      'result3': result3,
                      'key': id, 'cat': cat,
                      'cat_list': cat_list,
                      'obj_list1': obj_list1,
                      'obj_list2': obj_list2,
                      'obj_list3': obj_list3,
                      'similar_menus': similar_menus,
                      'page_nearby_range': page_nearby_range}
                  )


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


def webhook(req):
    print('webhook is running!')
    
    sh_file = '/home/www/food_master/webhook.sh'
    os.system(('cd /home/www/food_master/ && ./webhook.sh'))
    msg = os.popen(sh_file).read()
    data = {'status': 'ok', 'message': msg}
    return HttpResponse(json.dumps(data), content_type="application/json")
