# Generated by Django 4.0.3 on 2022-04-01 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_query_options_rename_name_query_query_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='query',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]