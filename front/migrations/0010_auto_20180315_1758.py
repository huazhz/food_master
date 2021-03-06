# Generated by Django 2.0.2 on 2018-03-15 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_auto_20180311_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brief', models.CharField(default='暂无', max_length=2048, verbose_name='简介')),
                ('notice', models.CharField(default='暂无', max_length=255, verbose_name='小贴士')),
            ],
        ),
        # migrations.RemoveField(
        #     model_name='recipe',
        #     name='brief',
        # ),
        # migrations.RemoveField(
        #     model_name='recipe',
        #     name='extra',
        # ),
        # migrations.RemoveField(
        #     model_name='recipe',
        #     name='notice',
        # ),
        migrations.AlterField(
            model_name='recipe',
            name='stars',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='details',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='recipe', to='front.RecipeDetails'),
        ),
    ]
