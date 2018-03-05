from django.contrib import admin

# Register your models here.
from .models import Member, Recipe, Ingredient, Nutrition, RecipeStep, RecipeTag, RecipeCategory, MemberRecipeList, \
    RecipeIngredient


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'email', 'brief_intro', 'join_ip', 'join_time')
    search_fields = ('name',)
    list_filter = ('gender', 'join_time', 'is_fake')
    date_hierarchy = 'join_time'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cover_img', 'rate_score', 'brief')
    search_fields = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", 'ingredient', 'usage')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'brief', 'benefits', 'choose_method', 'storage_duration', 'nutrition_knowledge')


class NutritionAdmin(admin.ModelAdmin):
    list_display = ('name', 'vol', 'add_time')


class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('step_detail', 'image_url', 'add_time')


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_time')


class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'add_time')


class MemberRecipeListAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_member', 'last_modify_time', 'add_time')


admin.site.register(Member, MemberAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Nutrition, NutritionAdmin)
admin.site.register(RecipeStep, RecipeStepAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeCategory, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(MemberRecipeList, MemberRecipeListAdmin)
