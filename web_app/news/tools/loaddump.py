import json

from django.core.exceptions import ObjectDoesNotExist

from news.models import Website


def parse_json():
    with open('dump.json') as f:
        data = json.load(f)
    return data


def add_websites(data):
    for elem in data:
        record = {
            'name': elem['name'],
            'url': elem['website'],
            'geo': elem['geo'],
            'available': elem['available'],
        }

        try:
            Website.objects.get(name=record['url'])
        except ObjectDoesNotExist:
            Website.objects.create(**record)


def run():
    data = parse_json()
    add_websites(data)

