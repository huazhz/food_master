#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Django-REST-Framework的序列化类
'''

from rest_framework import serializers
from front.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ serializer for recipe """
    
    class Meta:
        model = Recipe
        fields = ('fid',
                  'name',
                  'cover_img',
                  'rate_score',
                  'stars'
                  )
