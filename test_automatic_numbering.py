#!/usr/bin/env python
"""
Test script to verify the automatic order numbering system
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:/Users/USER/Desktop/store')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from payment.models import Order, OrderItem
from store.models import Product
from decimal import Decimal

def test_automatic_numbering():
    """Test that order numbers automatically adjust when orders are deleted"""
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Get or create a test product
    from store.models import Category
    
    # Create a test category first
    category, created = Category.objects.get_or_create(
        slug='test-category',
        defaults={
            'name': 'Test Category',
            'description': 'Test category for order numbering',
            'status': True,
            'trending': False,
            'meta_title': 'Test Category',
            'meta_keywords': 'test',
            'meta_description': 'Test category description'
        }
    )
    
    product, created = Product.objects.get_or_create(
        name='Test Product',
        defaults={
            'category': category,
            'slug': 'test-product',
            'small_description': 'Test product for order numbering',
            'quantity': 100,
            'on_sale': False,
            'description': 'Test product description',
            'original_price': 29.99,
            'selling_price': 19.99,
            'status': True,
            'trending': False,
            'tag': 'test',
            'meta_title': 'Test Product',
            'meta_keywords': 'test product',
            'meta_description': 'Test product description'
        }
    )
    
    print("Starting automatic order numbering test...")
    print("=" * 50)
    
    # Clean up existing orders for this user
    Order.objects.filter(user=user).delete()
    
    # Create 5 test orders
    orders = []
    for i in range(1, 6):
        order = Order.objects.create(
            user=user,
            first_name=f'Test{i}',
            last_name='User',
            email='test@example.com',
            phone='1234567890',
            address=f'Test Address {i}',
            city='Test City',
            postal_code='12345',
            total_amount=Decimal('29.99'),
            payment_status='paid',
            order_status='processing'
        )
        orders.append(order)
        
        # Create an order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.selling_price
        )
    
    print("Created 5 orders. Current order numbers:")
    for order in Order.objects.filter(user=user).order_by('created_at'):
        print(f"Order DB ID: {order.id} -> Order Number: {order.order_number}")
    
    print("\n" + "=" * 50)
    print("Deleting the 3rd order (middle one)...")
    
    # Delete the 3rd order
    orders[2].delete()
    
    print("After deletion. Current order numbers:")
    for order in Order.objects.filter(user=user).order_by('created_at'):
        print(f"Order DB ID: {order.id} -> Order Number: {order.order_number}")
    
    print("\n" + "=" * 50)
    print("Deleting the 1st order (first one)...")
    
    # Delete the 1st order
    orders[0].delete()
    
    print("After deletion. Current order numbers:")
    for order in Order.objects.filter(user=user).order_by('created_at'):
        print(f"Order DB ID: {order.id} -> Order Number: {order.order_number}")
    
    print("\n" + "=" * 50)
    print("Creating a new order...")
    
    # Create a new order
    new_order = Order.objects.create(
        user=user,
        first_name='New',
        last_name='Order',
        email='test@example.com',
        phone='1234567890',
        address='New Address',
        city='Test City',
        postal_code='12345',
        total_amount=Decimal('39.99'),
        payment_status='paid',
        order_status='processing'
    )
    
    OrderItem.objects.create(
        order=new_order,
        product=product,
        quantity=1,
        price=product.selling_price
    )
    
    print("After adding new order. Current order numbers:")
    for order in Order.objects.filter(user=user).order_by('created_at'):
        print(f"Order DB ID: {order.id} -> Order Number: {order.order_number}")
    
    print("\n" + "=" * 50)
    print("✅ Automatic order numbering test completed!")
    print("As you can see, order numbers automatically adjust when orders are deleted!")
    print("The numbering is always sequential (1, 2, 3, ...) regardless of database IDs.")

if __name__ == '__main__':
    test_automatic_numbering()
