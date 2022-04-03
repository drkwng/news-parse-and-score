from django.contrib import admin

from news.tools import check_avail, get_serp_data

from .models import Website, Query, QueryCheck


def check_website(self, request, queryset):
    queryset.update(available=False)
    for element in queryset.all():
        check_avail.run(url=element.url)
    self.message_user(request, "Websites available status has been checked")


def get_serp(self, request, queryset):
    for element in queryset.all():
        query = element.query
        location = element.location

        websites_obj = Website.objects.all()
        websites = [website.url for website in websites_obj if website.available]

        for website in websites:
            get_serp_data.run(
                url=website,
                keyword=query,
                location=location
            )
    self.message_user(request, "SERP Data parsing has been finished")


check_website.short_description = 'Check website available status'
get_serp.short_description = 'Get SERP Data'


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('name', 'available', 'website_link', 'geo', 'notes')
    list_display_links = ('name', )
    list_filter = ('available',)
    search_fields = ('name', 'url', 'geo')
    list_editable = ('available', 'notes')

    actions = (check_website, )


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'location')
    search_fields = ('query', )

    actions = (get_serp, )


@admin.register(QueryCheck)
class QueryCheckAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('query', 'website_link', 'format_serp', 'score', 'notes', 'date_check')
    list_filter = ('query', 'date_check')
    list_editable = ('score', 'notes')


admin.site.site_header = "Website Topics Score Tool"
admin.site.site_title = "Website Topics Score Tool"
admin.site.index_title = "Welcome to Website Topics Score Tool by @drkwng"
