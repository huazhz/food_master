from django.db import models
from django.db.models.functions import Now

class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Recipe(models.Model):
    """ 菜谱 """
    fid = models.CharField('外部id', max_length=64, null=True)
    name = models.CharField('名称', max_length=64, null=False)
    cover_img = models.CharField('封面图片', max_length=255, null=False)
    rate_score = models.CharField('综合评分', max_length=8, default='5')
    brief = models.CharField('简介', max_length=512, null=False)
    cook = models.ForeignKey(to=Member, null=True, on_delete=models.DO_NOTHING,
                             db_constraint=False, related_name='created_recipe')
    # 因为食谱和原谅有一个用量的关联关系，所以用到了through这个参数。
    ingredients = models.ManyToManyField(to='Ingredient', through='RecipeIngredient',
                                         through_fields=('recipe', 'ingredient'),
                                         db_constraint=False)
    recipe_ingredient = models.ForeignKey(to='RecipeIngredient', null=True, on_delete=models.DO_NOTHING,
                                          db_constraint=False)
    fav_by = models.ForeignKey(to='Member', on_delete=models.DO_NOTHING, db_constraint=False,
                               related_name='collected_recipe')
    notice = models.CharField('小贴士', max_length=255, default='暂无')
    extra = models.CharField('预留字段', max_length=16, default='暂无')
    add_time = models.DateTimeField(auto_now_add=True)


class Ingredient(models.Model):
    """ 原料 """
    name = models.CharField('名称', max_length=16, null=False)
    brief = models.CharField('名称', max_length=512, null=False)
    nutrition = models.ManyToManyField(to='Nutrition', on_delete=models.DO_NOTHING, db_constraint=False)
    benefits = models.CharField('功效好处描述', max_length=512, default='暂无')
    choose_method = models.CharField('如何挑选食材', max_length=2048, default='暂无')
    storage_method = models.CharField('储存方法', max_length=2048, default='暂无')
    storage_duration = models.CharField('名称', max_length=16, default='暂无')
    nutrition_knowledge = models.CharField('食材营养小知识', max_length=2048, default='暂无')
    suitable_people = models.CharField('使用人群', max_length=2048, default='暂无')
    cautions = models.CharField('饮食宜忌', max_length=2048, default='暂无')
    tips = models.CharField('食材烹饪小窍门', max_length=2048, default='暂无')
    add_time = models.DateTimeField(auto_now_add=True)

class Nutrition(models.Model):
    """ 营养原型 """
    name = models.CharField('名称', max_length=12, null=False)
    vol = models.CharField('含量', max_length=64, null=False)
    add_time = models.DateTimeField(auto_now_add=True)


class RecipeIngredient(models.Model):
    """ 菜谱和食材的关联关系 """
    recipe = models.ForeignKey(to='Recipe', on_delete=models.DO_NOTHING, db_constraint=False)
    ingredient = models.ForeignKey(to='Ingredient', on_delete=models.DO_NOTHING, db_constraint=False)
    usage = models.CharField('用量', max_length=64, null=False)



class RecipeStep(models.Model):
    """ 菜谱的步骤 n:1 菜谱"""
    name = models.CharField('名称', max_length=64, null=False)
    step_order = models.IntegerField('步骤的序号')
    image_url = models.CharField('步骤图示', null=True, max_length=255)
    recipe = models.ForeignKey(to='Recipe', on_delete=models.DO_NOTHING, db_constraint=False)


class RecipeTag(models.Model):
    """ 菜谱的标签 n:m 菜谱"""
    name = models.CharField('名称', max_length=64, null=False)


class RecipeCategory(models.Model):
    """ 菜谱的分类 n:m 菜谱"""
    name = models.CharField('名称', max_length=64, null=False)


class CategorySort(models.Model):
    """ 菜谱的分类的分类 n:m 分类"""
    name = models.CharField('名称', max_length=64, null=False)


class MemberRecipeList(models.Model):
    """ 用户创建的菜谱菜单 n:1 用户"""
    fid = models.CharField('外部id', max_length=64, null=True)
    name = models.CharField('名称', max_length=64, null=False)
    created_member = models.ForeignKey(to=Member, null=True, on_delete=models.DO_NOTHING,
                                       db_constraint=False,
                                       related_name='created_recipe_list')
    recipes = models.ManyToManyField(to='Recipe', related_name='included_in_list', db_constraint=False)
    fav_by = models.ForeignKey(to='Member', on_delete=models.DO_NOTHING, db_constraint=False,
                               related_name='collected_lists')
    last_modify_time = models.DateTimeField(default=Now())
    add_time = models.DateTimeField(auto_now_add=True)



