from django.apps import AppConfig
from django.core.management import call_command


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'
    
    # def ready(self):
    #     call_command('import_data')
