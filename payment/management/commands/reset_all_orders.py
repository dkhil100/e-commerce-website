from django.core.management.base import BaseCommand
from django.db import connection, transaction
from payment.models import Order, OrderItem, Payment


class Command(BaseCommand):
    help = 'Delete all orders and reset order ID sequence to start from 1'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion of all orders',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL orders and reset the order ID sequence.\n'
                    'Run with --confirm to proceed.'
                )
            )
            return

        # Count existing orders
        order_count = Order.objects.count()
        payment_count = Payment.objects.count()
        order_item_count = OrderItem.objects.count()

        if order_count == 0:
            self.stdout.write(
                self.style.WARNING('No orders found to delete.')
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Found {order_count} orders, {payment_count} payments, '
                    f'and {order_item_count} order items to delete.'
                )
            )

        # Delete all orders (this will cascade to OrderItems and Payments)
        with transaction.atomic():
            Order.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Successfully deleted all orders and related data.')
            )

            # Reset the auto-increment sequence
            with connection.cursor() as cursor:
                if connection.vendor == 'sqlite':
                    # For SQLite - reset sequences for all related tables
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_order';")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_orderitem';")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_payment';")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully reset ID sequences for SQLite')
                    )
                elif connection.vendor == 'postgresql':
                    # For PostgreSQL
                    cursor.execute("ALTER SEQUENCE payment_order_id_seq RESTART WITH 1;")
                    cursor.execute("ALTER SEQUENCE payment_orderitem_id_seq RESTART WITH 1;")
                    cursor.execute("ALTER SEQUENCE payment_payment_id_seq RESTART WITH 1;")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully reset ID sequences for PostgreSQL')
                    )
                elif connection.vendor == 'mysql':
                    # For MySQL
                    cursor.execute("ALTER TABLE payment_order AUTO_INCREMENT = 1;")
                    cursor.execute("ALTER TABLE payment_orderitem AUTO_INCREMENT = 1;")
                    cursor.execute("ALTER TABLE payment_payment AUTO_INCREMENT = 1;")
                    self.stdout.write(
                        self.style.SUCCESS('Successfully reset ID sequences for MySQL')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Database vendor {connection.vendor} is not supported')
                    )
                    return

        self.stdout.write(
            self.style.SUCCESS(
                'All orders deleted and ID sequences reset. Next order will have ID 1.'
            )
        )
