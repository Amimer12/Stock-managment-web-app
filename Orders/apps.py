from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Orders'
    verbose_name = "Gestion des Commandes"
    def ready(self):
        import Orders.signals
