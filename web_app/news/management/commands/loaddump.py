from django.core.management.base import BaseCommand
from news.tools.loaddump import run


class Command(BaseCommand):
    help = 'Load dump data from json'

    def handle(self, *args, **options):
        run()
