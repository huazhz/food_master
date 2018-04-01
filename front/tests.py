from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest

from .views import index
from .models import Recipe, RecipeCategory, RecipeDetails, RecipeIngredient, RecipeStep, RecipeTag, Member, \
    CategoryType, MemberRecipeList, Ingredient, Nutrition


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.factory = RequestFactory()
    
    def test_index1(self):
        ''' try Client '''
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)
    
    def test_index2(self):
        ''' try RequestFactory '''
        response2 = self.factory.get('/')
        print(self.factory.request().method)
        print(self.factory.request().path)
        print(self.factory.request().build_absolute_uri())
        print(response2.path)
        print(response2.environ)
        print(response2.body)
    
    def test_index3(self):
        ''' 尝试第3种测试方法 '''
        request = HttpRequest()
        response = index(request)
        print(response.status_code)
        print(response.content)
    
    def tearDown(self):
        pass
