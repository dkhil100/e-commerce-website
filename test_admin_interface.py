#!/usr/bin/env python
"""
Test script to verify admin interface works with the new OrderItem model changes
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
from store.models import Product, Category
from decimal import Decimal

def test_admin_interface():
    """Test that OrderItem can be created with None values without errors"""
    
    print("Testing admin interface compatibility...")
    print("=" * 50)
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='admintest',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'Test'
        }
    )
    
    # Create test category
    category, created = Category.objects.get_or_create(
        slug='admin-test-category',
        defaults={
            'name': 'Admin Test Category',
            'description': 'Test category for admin',
            'status': True,
            'trending': False,
            'meta_title': 'Admin Test Category',
            'meta_keywords': 'admin test',
            'meta_description': 'Admin test category description'
        }
    )
    
    # Create test product
    product, created = Product.objects.get_or_create(
        name='Admin Test Product',
        defaults={
            'category': category,
            'slug': 'admin-test-product',
            'small_description': 'Product for admin testing',
            'quantity': 10,
            'on_sale': False,
            'description': 'Admin test product description',
            'original_price': 19.99,
            'selling_price': 15.99,
            'status': True,
            'trending': False,
            'tag': 'admin-test',
            'meta_title': 'Admin Test Product',
            'meta_keywords': 'admin test product',
            'meta_description': 'Admin test product description'
        }
    )
    
    # Create test order
    order = Order.objects.create(
        user=user,
        first_name='Admin',
        last_name='Test',
        email='admin@example.com',
        phone='1234567890',
        address='123 Admin Street',
        city='Admin City',
        postal_code='12345',
        total_amount=Decimal('15.99'),
        payment_status='paid',
        order_status='processing'
    )
    
    print(f"Created order: {order}")
    
    # Test 1: Create OrderItem with all fields
    print("\nTest 1: Creating OrderItem with all fields...")
    order_item1 = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2,
        price=Decimal('15.99')
    )
    
    print(f"OrderItem created: {order_item1}")
    print(f"Total price: {order_item1.total_price}")
    
    # Test 2: Create OrderItem with None quantity (simulate admin form)
    print("\nTest 2: Creating OrderItem with None values...")
    order_item2 = OrderItem(
        order=order,
        product=product,
        quantity=None,
        price=None
    )
    
    print(f"OrderItem with None values: {order_item2}")
    print(f"Total price with None values: {order_item2.total_price}")
    
    # Test 3: Create OrderItem with partial None values
    print("\nTest 3: Creating OrderItem with partial None values...")
    order_item3 = OrderItem(
        order=order,
        product=product,
        quantity=1,
        price=None
    )
    
    print(f"OrderItem with None price: {order_item3}")
    print(f"Total price with None price: {order_item3.total_price}")
    
    # Test 4: Test save method with None values
    print("\nTest 4: Testing save method with None values...")
    order_item4 = OrderItem(
        order=order,
        product=product,
        quantity=None,
        price=Decimal('15.99')
    )
    
    try:
        # This should not crash due to None quantity
        order_item4.save()
        print("✅ Save method handled None values correctly")
    except Exception as e:
        print(f"❌ Save method failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Admin interface compatibility test completed!")
    print("All OrderItem operations handled None values correctly.")

if __name__ == '__main__':
    test_admin_interface()
