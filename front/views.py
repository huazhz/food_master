from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from front.models import Recipe, RecipeIngredient

from front import rs


# Create your views here.
# I know, shut your mouth.
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


def generic(req):
    """ 首页 """
    
    return render(req, 'front/recipe.html')


def elements(req):
    """ 首页 """
    
    return render(req, 'front/elements.html')


def search_result(req, key, page_num):
    """ 搜索列表展示页"""
    obj_list = Recipe.objects.filter(name__contains=key).order_by('-rate_score')
    paginator = Paginator(obj_list, 10)
    result = paginator.get_page(page_num)
    # return HttpResponse(result)
    return render(req, 'front/list.html', context={'result': result, 'key': key})


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
