#!/usr/bin/env python
"""
Test script to verify quantity management and sold out functionality
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

def test_quantity_management():
    """Test that product quantities decrease when orders are placed"""
    
    print("Starting quantity management test...")
    print("=" * 50)
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Create a test category
    category, created = Category.objects.get_or_create(
        slug='test-category',
        defaults={
            'name': 'Test Category',
            'description': 'Test category for quantity management',
            'status': True,
            'trending': False,
            'meta_title': 'Test Category',
            'meta_keywords': 'test',
            'meta_description': 'Test category description'
        }
    )
    
    # Create a test product with initial quantity of 10
    product, created = Product.objects.get_or_create(
        name='Test Product for Quantity',
        defaults={
            'category': category,
            'slug': 'test-product-quantity',
            'small_description': 'Test product for quantity management',
            'quantity': 10,
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
    
    if not created:
        # Reset quantity for testing
        product.quantity = 10
        product.save()
    
    print(f"Initial product quantity: {product.quantity}")
    print(f"Initial sold_out status: {product.sold_out}")
    
    # Test 1: Create an order with 3 items
    print("\n" + "=" * 50)
    print("Test 1: Creating order with 3 items")
    
    order1 = Order.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        phone='1234567890',
        address='Test Address',
        city='Test City',
        postal_code='12345',
        total_amount=Decimal('59.97'),
        payment_status='paid',
        order_status='processing'
    )
    
    OrderItem.objects.create(
        order=order1,
        product=product,
        quantity=3,
        price=product.selling_price
    )
    
    # Refresh product from database
    product.refresh_from_db()
    
    print(f"After order 1 - Product quantity: {product.quantity}")
    print(f"After order 1 - Sold out status: {product.sold_out}")
    
    # Test 2: Create another order with 5 items
    print("\n" + "=" * 50)
    print("Test 2: Creating order with 5 items")
    
    order2 = Order.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        phone='1234567890',
        address='Test Address',
        city='Test City',
        postal_code='12345',
        total_amount=Decimal('99.95'),
        payment_status='paid',
        order_status='processing'
    )
    
    OrderItem.objects.create(
        order=order2,
        product=product,
        quantity=5,
        price=product.selling_price
    )
    
    # Refresh product from database
    product.refresh_from_db()
    
    print(f"After order 2 - Product quantity: {product.quantity}")
    print(f"After order 2 - Sold out status: {product.sold_out}")
    
    # Test 3: Create an order with remaining items (should make it sold out)
    print("\n" + "=" * 50)
    print("Test 3: Creating order with remaining items")
    
    order3 = Order.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        phone='1234567890',
        address='Test Address',
        city='Test City',
        postal_code='12345',
        total_amount=Decimal('39.98'),
        payment_status='paid',
        order_status='processing'
    )
    
    OrderItem.objects.create(
        order=order3,
        product=product,
        quantity=2,
        price=product.selling_price
    )
    
    # Refresh product from database
    product.refresh_from_db()
    
    print(f"After order 3 - Product quantity: {product.quantity}")
    print(f"After order 3 - Sold out status: {product.sold_out}")
    
    # Test 4: Test availability method
    print("\n" + "=" * 50)
    print("Test 4: Testing availability method")
    
    print(f"Product is_available(): {product.is_available()}")
    
    print("\n" + "=" * 50)
    print("✅ Quantity management test completed!")
    print("Summary:")
    print(f"- Initial quantity: 10")
    print(f"- Order 1: -3 items = 7 remaining")
    print(f"- Order 2: -5 items = 2 remaining")
    print(f"- Order 3: -2 items = 0 remaining (SOLD OUT)")
    print(f"- Final quantity: {product.quantity}")
    print(f"- Final sold_out status: {product.sold_out}")
    print(f"- Product available: {product.is_available()}")

if __name__ == '__main__':
    test_quantity_management()
