# Generated by Django 2.0.2 on 2018-02-27 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_auto_20180227_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='nutrition',
            name='name',
            field=models.CharField(max_length=128, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=128, verbose_name='名称'),
        ),
    ]
