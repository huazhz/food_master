# Generated by Django 2.0.2 on 2018-02-27 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '菜谱菜单分类',
                'ordering': ['add_time'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='名称')),
                ('brief', models.CharField(default='暂无', max_length=512, verbose_name='简介')),
                ('benefits', models.CharField(default='暂无', max_length=512, verbose_name='功效好处描述')),
                ('choose_method', models.CharField(default='暂无', max_length=2048, verbose_name='如何挑选食材')),
                ('storage_method', models.CharField(default='暂无', max_length=2048, verbose_name='储存方法')),
                ('storage_duration', models.CharField(default='暂无', max_length=16, verbose_name='名称')),
                ('nutrition_knowledge', models.CharField(default='暂无', max_length=2048, verbose_name='食材营养小知识')),
                ('suitable_people', models.CharField(default='暂无', max_length=2048, verbose_name='使用人群')),
                ('cautions', models.CharField(default='暂无', max_length=2048, verbose_name='饮食宜忌')),
                ('tips', models.CharField(default='暂无', max_length=2048, verbose_name='食材烹饪小窍门')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '食材',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('gender', models.CharField(max_length=20, verbose_name='性别')),
                ('email', models.EmailField(max_length=24, null=True, verbose_name='邮箱')),
                ('mobile', models.EmailField(max_length=16, null=True, verbose_name='手机号')),
                ('password', models.CharField(max_length=64, null=True, verbose_name='明文密码')),
                ('md5_password', models.CharField(max_length=64, null=True, verbose_name='加密密码')),
                ('is_fake', models.IntegerField(default=0, verbose_name='如果是爬虫抓的话，就给这个字段1')),
                ('brief_intro', models.CharField(max_length=255, verbose_name='个人简介')),
                ('join_ip', models.CharField(max_length=16, verbose_name='加入ip')),
                ('join_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
            ],
            options={
                'verbose_name_plural': '会员',
                'ordering': ['join_time'],
            },
        ),
        migrations.CreateModel(
            name='MemberRecipeList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.CharField(max_length=64, null=True, verbose_name='外部id')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('last_modify_time', models.DateTimeField(auto_now_add=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('created_member', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_recipe_list', to='front.Member')),
                ('fav_by', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collected_lists', to='front.Member')),
            ],
            options={
                'verbose_name_plural': '用户创建的菜谱菜单',
                'ordering': ['add_time'],
            },
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('vol', models.CharField(max_length=64, verbose_name='含量')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '营养成分',
                'ordering': ['add_time'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.CharField(max_length=64, null=True, verbose_name='外部id')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('cover_img', models.CharField(max_length=255, verbose_name='封面图片')),
                ('rate_score', models.CharField(default='5', max_length=8, verbose_name='综合评分')),
                ('brief', models.CharField(max_length=512, verbose_name='简介')),
                ('notice', models.CharField(default='暂无', max_length=255, verbose_name='小贴士')),
                ('extra', models.CharField(default='暂无', max_length=16, verbose_name='预留字段')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '菜谱',
                'ordering': ['add_time'],
            },
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('category_type', models.ManyToManyField(db_constraint=False, to='front.CategoryType')),
            ],
            options={
                'verbose_name_plural': '菜谱分类',
                'ordering': ['add_time'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(max_length=64, null=True, verbose_name='用量')),
                ('ingredient', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='front.Ingredient')),
                ('recipe', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='front.Recipe')),
            ],
            options={
                'verbose_name_plural': '菜谱食材关联关系',
            },
        ),
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_order', models.IntegerField(verbose_name='步骤的序号')),
                ('step_detail', models.CharField(default='暂无', max_length=2048, verbose_name='步骤详情')),
                ('image_url', models.CharField(max_length=255, null=True, verbose_name='步骤图示')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='front.Recipe')),
            ],
            options={
                'verbose_name_plural': '步骤',
                'ordering': ['add_time'],
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '标签',
                'ordering': ['add_time'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.ManyToManyField(to='front.RecipeCategory'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='cook',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_recipe', to='front.Member'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fav_by',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collected_recipe', to='front.Member'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='front.RecipeIngredient', to='front.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(db_constraint=False, to='front.RecipeTag'),
        ),
        migrations.AddField(
            model_name='memberrecipelist',
            name='recipes',
            field=models.ManyToManyField(db_constraint=False, related_name='included_in_list', to='front.Recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('name', 'brief_intro')},
        ),
        migrations.AddField(
            model_name='ingredient',
            name='nutrition',
            field=models.ManyToManyField(db_constraint=False, to='front.Nutrition'),
        ),
        migrations.AlterUniqueTogether(
            name='recipeingredient',
            unique_together={('recipe', 'usage', 'ingredient')},
        ),
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together={('name', 'fid')},
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('name', 'brief')},
        ),
    ]
