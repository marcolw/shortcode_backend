from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import requests

from shortcode.operations import import_from_url
from shortcode.models import AdminSetting


class Command(BaseCommand):
    def handle(self, *args, **options):
        setting = AdminSetting.objects.first()
        import_from_url(setting.import_url)
