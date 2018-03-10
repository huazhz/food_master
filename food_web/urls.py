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
from django.urls import path
from front import views
from utils import common_utils



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('category/<int:id>/', views.category),
    path('category/<int:id>/<int:page_num>/', views.category),
    path('search/<str:key>/', views.search_result),
    path('search/<str:key>/<int:page_num>/', views.search_result),
    path('recipe/<int:id>/', views.recipe_details)


]
handler500 = common_utils.handle_500
handler404 = common_utils.handle_404
