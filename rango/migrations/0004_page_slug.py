# Generated by Django 3.0.2 on 2020-02-04 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_auto_20200203_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
