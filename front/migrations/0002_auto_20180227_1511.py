# Generated by Django 2.0.2 on 2018-02-27 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recipestep',
            unique_together={('image_url', 'step_order', 'recipe')},
        ),
    ]
