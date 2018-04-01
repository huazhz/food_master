from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.http import HttpRequest

from .views import index
from .models import Recipe, RecipeCategory, RecipeDetails, RecipeIngredient, RecipeStep, RecipeTag, Member, \
    CategoryType, MemberRecipeList, Ingredient, Nutrition


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
    
    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200
    
    def tearDown(self):
        pass
