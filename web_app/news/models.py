from django.db import models
from django.utils.html import format_html
from django.core.validators import MaxValueValidator, MinValueValidator


GEO_CHOICES = (
    ('United States', 'USA'),
    ('New York,New York,United States', 'USA, New York'),
    ('Los Angeles,California,United States', 'USA, Los Angeles (CA)'),
    ('London,England,United Kingdom', 'UK, London'),
    ('Paris,Ile-de-France,France', 'France, Paris')
)


class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    geo = models.CharField(max_length=255)
    available = models.BooleanField(default=False)
    notes = models.TextField(default='', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def website_link(self):
        """ This returns a HTML anchor (hyperlink) to somewhere """
        return format_html(f'<a href="{self.url}" target="_blank">{self.url}</a>')


class Query(models.Model):
    query = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, choices=GEO_CHOICES, default='United States')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "queries"

    def __str__(self):
        return self.query


class QueryCheck(models.Model):
    query = models.ForeignKey(Query, null=True, on_delete=models.CASCADE)
    date_check = models.DateTimeField(auto_now_add=True)
    website = models.ForeignKey(Website, null=True, on_delete=models.CASCADE)
    serp_data = models.TextField()
    score = models.IntegerField(default=1,
                                validators=[MaxValueValidator(10), MinValueValidator(1)])
    notes = models.TextField(default='', blank=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.website.url} ({self.query.query})'

    def website_link(self):
        """ This returns a HTML anchor (hyperlink) to somewhere """
        return format_html(f'<a href="{self.website.url}" target="_blank">{self.website.name}</a>')

    def format_serp(self):
        """ HTML formatting for SERP Data """
        return format_html(self.serp_data)
