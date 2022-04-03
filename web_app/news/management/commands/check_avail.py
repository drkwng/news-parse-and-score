from django.core.management.base import BaseCommand

from news.tools.check_avail import run


class Command(BaseCommand):
    help = 'Check website available status'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=int)

    def handle(self, *args, **options):
        run(*args)
