#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Django-REST-Framework的序列化类
'''

from rest_framework import serializers
from front.models import Recipe, Member
import time


class RecipeSerializer(serializers.ModelSerializer):
    """ serializer for recipe """
    cookname = serializers.CharField(source='cook.name')
    
    class Meta:
        model = Recipe
        fields = ('fid',
                  'cook',
                  'cookname',
                  'name',
                  'cover_img',
                  'rate_score',
                  'stars'
                  )
        depth = 1
