from django.apps import AppConfig


class UsersprofilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UsersProfiles'
    
    def ready(self):
        import UsersProfiles.signals
        