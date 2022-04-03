# Generated by Django 4.0.3 on 2022-04-01 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_website_available_alter_website_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('date_check', models.DateTimeField(auto_now_add=True)),
                ('serp_data', models.TextField()),
                ('website', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='serp_checks', to='news.website')),
            ],
        ),
        migrations.CreateModel(
            name='WebsiteCheckScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('notes', models.TextField()),
                ('query_check', models.ManyToManyField(to='news.querycheck')),
            ],
        ),
        migrations.DeleteModel(
            name='SERPData',
        ),
    ]