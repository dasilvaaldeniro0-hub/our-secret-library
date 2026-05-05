from django.apps import AppConfig

class LibraryAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library_app'

    def ready(self):
        from .create_admin import create_admin
        try:
            create_admin()
        except:
            pass