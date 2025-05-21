from django.apps import AppConfig

class TodosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todos'
    verbose_name = "Todo Manager Pro"  # Nicer name in Admin

    def ready(self):
        # Runs when Django starts (DEV: runs twice, avoid DB calls in production)
        if not self._is_running_test():  # Skip during tests
            self.create_default_categories()

    def create_default_categories(self):
        from .models import Category
        default_categories = ["Personal", "Work", "Shopping"]
        for name in default_categories:
            Category.objects.get_or_create(name=name)

    def _is_running_test(self):
        import sys
        return 'test' in sys.argv
