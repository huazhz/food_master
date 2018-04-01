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
        '''
            try Client
        '''
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)
        print(' 1st test pass ')
    
    def test_index2(self):
        '''
            try RequestFactory
        '''
        response2 = self.factory.get('/')
        self.assertEqual(response2.path, '/')
        self.assertEqual(self.factory.request().method, 'GET')
        print('2nd test pass')
    
    def test_index3(self):
        '''
            尝试第3种测试方法
        '''
        request = HttpRequest()
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('菜谱大全', response.content.decode('utf8'))
        print(' 3rd test pass')
    
    def tearDown(self):
        pass
