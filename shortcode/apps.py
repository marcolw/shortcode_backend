from django.apps import AppConfig


class ShortcodeConfig(AppConfig):
    name = 'shortcode'

    def ready(self):
        from . import signals
