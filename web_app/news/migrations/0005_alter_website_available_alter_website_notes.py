# Generated by Django 4.0.3 on 2022-03-31 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_website_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='website',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
    ]
