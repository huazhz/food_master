from django.db import models
from django.db.models.functions import Now


class Member(models.Model):
    name = models.CharField('姓名', max_length=12)
    gender = models.CharField('性别', max_length=4)
    email = models.EmailField('邮箱', max_length=24, null=True)
    mobile = models.EmailField('手机号', max_length=16, null=True)
    password = models.CharField('明文密码', max_length=64, null=True)
    md5_password = models.CharField('加密密码', max_length=64, null=True)
    is_fake = models.IntegerField('如果是爬虫抓的话，就给这个字段1', default=0)
    brief_intro = models.CharField('个人简介', max_length=255)
    join_ip = models.CharField('加入ip', max_length=16)
    join_time = models.DateTimeField('加入时间', auto_now_add=True)
    
    class Meta:
        ordering = ['join_time']
        verbose_name_plural = '会员'
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ 菜谱 """
    fid = models.CharField('外部id', max_length=64, null=True)
    name = models.CharField('名称', max_length=64, null=False)
    cover_img = models.CharField('封面图片', max_length=255, null=False)
    rate_score = models.CharField('综合评分', max_length=8, default='5')
    brief = models.CharField('简介', max_length=512, null=False)
    cook = models.ForeignKey(to=Member, null=True, on_delete=models.DO_NOTHING,
                             db_constraint=False, related_name='created_recipe')
    # 因为食谱和原料有一个用量的关联关系，所以用到了through这个参数。
    ingredients = models.ManyToManyField(to='Ingredient', through='RecipeIngredient',
                                         through_fields=('recipe', 'ingredient'))
    category = models.ManyToManyField(to='RecipeCategory')
    fav_by = models.ForeignKey(to='Member', on_delete=models.DO_NOTHING, db_constraint=False,
                               related_name='collected_recipe')
    notice = models.CharField('小贴士', max_length=255, default='暂无')
    tag = models.ManyToManyField(to='RecipeTag', db_constraint=False)
    extra = models.CharField('预留字段', max_length=16, default='暂无')
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '菜谱'
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ 原料 """
    name = models.CharField('名称', max_length=16, null=False, unique=True)
    brief = models.CharField('简介', max_length=512, null=False)
    nutrition = models.ManyToManyField(to='Nutrition', db_constraint=False)
    benefits = models.CharField('功效好处描述', max_length=512, default='暂无')
    choose_method = models.CharField('如何挑选食材', max_length=2048, default='暂无')
    storage_method = models.CharField('储存方法', max_length=2048, default='暂无')
    storage_duration = models.CharField('名称', max_length=16, default='暂无')
    nutrition_knowledge = models.CharField('食材营养小知识', max_length=2048, default='暂无')
    suitable_people = models.CharField('使用人群', max_length=2048, default='暂无')
    cautions = models.CharField('饮食宜忌', max_length=2048, default='暂无')
    tips = models.CharField('食材烹饪小窍门', max_length=2048, default='暂无')
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = '食材'
    
    def __str__(self):
        return self.name


class Nutrition(models.Model):
    """ 营养原型 """
    name = models.CharField('名称', max_length=12, null=False)
    vol = models.CharField('含量', max_length=64, null=False)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '营养成分'
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """ 菜谱的食材用量 """
    recipe = models.ForeignKey(to='Recipe', on_delete=models.DO_NOTHING, db_constraint=False)
    ingredient = models.ForeignKey(to='Ingredient', on_delete=models.DO_NOTHING, db_constraint=False)
    usage = models.CharField('用量', max_length=64, null=False)
    
    class Meta:
        verbose_name_plural = '菜谱食材关联关系'
    
    def __str__(self):
        return self.recipe.name


class RecipeStep(models.Model):
    """ 菜谱的步骤 n:1 菜谱"""
    # name = models.CharField('名称', max_length=64, null=False)
    step_order = models.IntegerField('步骤的序号')
    step_detail = models.CharField('步骤详情', max_length=2048, default='暂无')
    image_url = models.CharField('步骤图示', null=True, max_length=255)
    recipe = models.ForeignKey(to='Recipe', on_delete=models.DO_NOTHING, db_constraint=False)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '步骤'
    
    def __str__(self):
        return self.step_detail


class RecipeTag(models.Model):
    """ 菜谱的标签 n:m 菜谱"""
    name = models.CharField('名称', max_length=64, null=False)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '标签'
    
    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    """ 菜谱的分类 n:m 菜谱"""
    name = models.CharField('名称', max_length=64, null=False)
    category_type = models.ManyToManyField(to='CategoryType', db_constraint=False)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '菜谱分类'
    
    def __str__(self):
        return self.name


class CategoryType(models.Model):
    """ 菜谱的分类的类型 n:m 分类"""
    name = models.CharField('名称', max_length=64, null=False)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '菜谱菜单分类'
    
    def __str__(self):
        return self.name


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
    last_modify_time = models.DateTimeField(auto_now_add=True)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['add_time']
        verbose_name_plural = '用户创建的菜谱菜单'
    
    def __str__(self):
        return self.name
