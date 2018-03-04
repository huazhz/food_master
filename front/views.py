from django.shortcuts import render
from django.http import Http404
from front.models import Recipe
from front import rs






# Create your views here.

def index(req):
    """ 首页 """

    return render(req,'front/index.html')



def generic(req):
    """ 首页 """

    return render(req, 'front/recipe.html')


def elements(req):
    """ 首页 """

    return render(req,'front/elements.html')

def recipe_details(req,id=None):
    if not id:
        return Http404
    recipe = Recipe.objects.get(id=id)
    category = recipe.category.all()
    first_cate = category[0] if category else None
    recipe_steps = recipe.recipestep_set.all()
    return render(req, 'front/recipe.html', locals())
