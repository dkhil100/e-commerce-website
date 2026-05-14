from django.core.management.base import BaseCommand
from django.db import connection
from payment.models import Order


class Command(BaseCommand):
    help = 'Reset order ID sequence to start from 1'

    def handle(self, *args, **options):
        # Check if there are any orders
        order_count = Order.objects.count()
        if order_count > 0:
            self.stdout.write(
                self.style.WARNING(f'There are {order_count} existing orders. Please delete all orders first or use --force to reset anyway.')
            )
            return

        # Reset the auto-increment sequence for different databases
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                # For SQLite
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
