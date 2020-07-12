from django.apps import AppConfig


class DataAppConfig(AppConfig):
    name = 'data'

    def ready(self):
        import data.signals
        import inspections.signals
        import accounts.signals