from django.core.management.base import BaseCommand

from news.tools.get_serp_data import run


class Command(BaseCommand):
    help = 'Get SERP Data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=int)
        parser.add_argument('keyword', nargs='+', type=int)
        parser.add_argument('location', nargs='+', type=int)

    def handle(self, *args, **options):
        run(*args)
