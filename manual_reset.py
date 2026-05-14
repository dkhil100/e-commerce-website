#!/usr/bin/env python
"""
Manually delete all orders and reset sequence
"""
import os
import sys
import django
from django.db import connection, transaction

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from payment.models import Order, OrderItem, Payment

def delete_all_orders_and_reset():
    """Delete all orders and reset the sequence"""
    print("🗑️  Deleting all orders and resetting sequence...")
    
    # Get counts before deletion
    order_count = Order.objects.count()
    payment_count = Payment.objects.count()
    order_item_count = OrderItem.objects.count()
    
    print(f"📊 Found: {order_count} orders, {payment_count} payments, {order_item_count} order items")
    
    # Delete all orders (this will cascade to OrderItems and Payments)
    with transaction.atomic():
        Order.objects.all().delete()
        print("✅ Deleted all orders and related data")
        
        # Reset the auto-increment sequence
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                # For SQLite - reset sequences for all related tables
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_order';")
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_orderitem';")
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='payment_payment';")
                print("✅ Reset SQLite sequences")
            elif connection.vendor == 'postgresql':
                # For PostgreSQL
                cursor.execute("ALTER SEQUENCE payment_order_id_seq RESTART WITH 1;")
                cursor.execute("ALTER SEQUENCE payment_orderitem_id_seq RESTART WITH 1;")
                cursor.execute("ALTER SEQUENCE payment_payment_id_seq RESTART WITH 1;")
                print("✅ Reset PostgreSQL sequences")
            elif connection.vendor == 'mysql':
                # For MySQL
                cursor.execute("ALTER TABLE payment_order AUTO_INCREMENT = 1;")
                cursor.execute("ALTER TABLE payment_orderitem AUTO_INCREMENT = 1;")
                cursor.execute("ALTER TABLE payment_payment AUTO_INCREMENT = 1;")
                print("✅ Reset MySQL sequences")
    
    print("🎉 All orders deleted and sequences reset. Next order will be #1")

if __name__ == '__main__':
    delete_all_orders_and_reset()
