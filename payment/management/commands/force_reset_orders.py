from django.core.management.base import BaseCommand
from django.db import connection, transaction
from payment.models import Order, OrderItem, Payment


class Command(BaseCommand):
    help = 'Force reset order ID sequence (use after manually deleting orders from admin)'

    def handle(self, *args, **options):
        # Delete any remaining orders and reset sequence
        order_count = Order.objects.count()
        
        with transaction.atomic():
            if order_count > 0:
                Order.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted {order_count} remaining orders')
                )
            
            # Reset the auto-increment sequence
            with connection.cursor() as cursor:
                if connection.vendor == 'sqlite':
                    # For SQLite - reset sequences for all related tables
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_order';")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_orderitem';")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_payment';")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully reset order ID sequence for SQLite')
                    )
                elif connection.vendor == 'postgresql':
                    # For PostgreSQL
                    cursor.execute("ALTER SEQUENCE payment_order_id_seq RESTART WITH 1;")
                    cursor.execute("ALTER SEQUENCE payment_orderitem_id_seq RESTART WITH 1;")
                    cursor.execute("ALTER SEQUENCE payment_payment_id_seq RESTART WITH 1;")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully reset order ID sequence for PostgreSQL')
                    )
                elif connection.vendor == 'mysql':
                    # For MySQL
                    cursor.execute("ALTER TABLE payment_order AUTO_INCREMENT = 1;")
                    cursor.execute("ALTER TABLE payment_orderitem AUTO_INCREMENT = 1;")
                    cursor.execute("ALTER TABLE payment_payment AUTO_INCREMENT = 1;")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully reset order ID sequence for MySQL')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Database vendor {connection.vendor} is not supported')
                    )
                    return

        self.stdout.write(
            self.style.SUCCESS('Order ID sequence has been reset. Next order will have ID 1.')
        )
