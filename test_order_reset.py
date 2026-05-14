#!/usr/bin/env python
"""
Test script to demonstrate order ID reset functionality
"""
import os
import sys
import django
from django.core.management import call_command

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from payment.models import Order, OrderItem, Payment

def main():
    print("🧪 Testing Order ID Reset Functionality...")
    
    # Show current order count
    order_count = Order.objects.count()
    print(f"📊 Current orders in database: {order_count}")
    
    if order_count > 0:
        print("\n📋 Current orders:")
        for order in Order.objects.all().order_by('id'):
            print(f"   Order #{order.id} - {order.full_name} - ${order.total_amount}")
    
    print("\n🗑️  To reset order IDs, you have two options:")
    print("\n1. Delete all orders and reset sequence:")
    print("   python manage.py reset_all_orders --confirm")
    
    print("\n2. If you already deleted orders via admin, reset sequence only:")
    print("   python manage.py reset_order_sequence")
    
    print("\n📝 Instructions:")
    print("1. Go to Django admin (/admin/)")
    print("2. Delete all orders manually, or")
    print("3. Use the management command above")
    print("4. Next order will start from ID #1")
    
    print("\n⚠️  Warning: This will permanently delete all order data!")

if __name__ == '__main__':
    main()
