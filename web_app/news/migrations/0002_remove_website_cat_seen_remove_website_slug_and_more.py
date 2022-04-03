# Generated by Django 4.0.3 on 2022-03-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='cat_seen',
        ),
        migrations.RemoveField(
            model_name='website',
            name='slug',
        ),
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.URLField(),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]