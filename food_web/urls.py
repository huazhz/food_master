"""food_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from front import views
from utils import common_utils
from rest_framework.schemas import get_schema_view
from front.views import RecipeAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/recipes', RecipeAPIView, base_name='recipe')

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('category/<int:id>/', views.category),
    path('category/<int:id>/<int:page_num>/', views.category),
    path('search/<str:key>/', views.search_result),
    path('search/<str:key>/<int:page_num>/', views.search_result),
    path('recipe/<int:id>/', views.recipe_details),
    path('sitemap/', views.sitemap),
    path('webhook/', views.webhook),

]

urlpatterns += router.urls

handler500 = common_utils.handle_500
handler404 = common_utils.handle_404
