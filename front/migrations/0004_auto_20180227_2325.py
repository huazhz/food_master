# Generated by Django 2.0.2 on 2018-02-27 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_auto_20180227_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='brief',
            field=models.CharField(max_length=2048, verbose_name='简介'),
        ),
    ]
