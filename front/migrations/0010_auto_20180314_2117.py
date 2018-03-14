# Generated by Django 2.0.2 on 2018-03-14 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_auto_20180311_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brief', models.CharField(default='暂无', max_length=2048, verbose_name='简介')),
                ('notice', models.CharField(default='暂无', max_length=255, verbose_name='小贴士')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='brief',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='notice',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cover_img',
            field=models.CharField(max_length=32, verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='extra',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='recipe', to='front.RecipeExtra'),
        ),
    ]
