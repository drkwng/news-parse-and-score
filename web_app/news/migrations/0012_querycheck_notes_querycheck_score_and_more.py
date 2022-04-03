# Generated by Django 4.0.3 on 2022-04-02 10:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_query_query_alter_website_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='querycheck',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='querycheck',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.DeleteModel(
            name='WebsiteCheckScore',
        ),
    ]
