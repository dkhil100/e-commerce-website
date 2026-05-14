#!/usr/bin/env python
"""
Test script to verify the complete checkout process with quantity management
"""
import os
import sys
import django
from django.test import Client

# Add the project directory to Python path
sys.path.append('c:/Users/USER/Desktop/store')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.urls import reverse
from payment.models import Order, OrderItem
from store.models import Product, Category
from cart.models import Cart, CartItem
from decimal import Decimal

def test_checkout_with_quantity_management():
    """Test checkout process with quantity management"""
    
    print("Starting checkout with quantity management test...")
    print("=" * 60)
    
    # Clean up any existing test data
    User.objects.filter(username='testuser').delete()
    
    # Create test user
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    
    # Create test category
    category, created = Category.objects.get_or_create(
        slug='test-category',
        defaults={
            'name': 'Test Category',
            'description': 'Test category',
            'status': True,
            'trending': False,
            'meta_title': 'Test Category',
            'meta_keywords': 'test',
            'meta_description': 'Test category description'
        }
    )
    
    # Create test product with limited quantity
    product, created = Product.objects.get_or_create(
        name='Limited Stock Product',
        defaults={
            'category': category,
            'slug': 'limited-stock-product',
            'small_description': 'Product with limited stock',
            'quantity': 3,  # Only 3 items available
            'on_sale': False,
            'description': 'Test product with limited stock',
            'original_price': 29.99,
            'selling_price': 19.99,
            'status': True,
            'trending': False,
            'tag': 'test',
            'meta_title': 'Limited Stock Product',
            'meta_keywords': 'limited stock test',
            'meta_description': 'Test product with limited stock'
        }
    )
    
    if not created:
        product.quantity = 3
        product.save()
    
    print(f"Created test product: {product.name}")
    print(f"Initial quantity: {product.quantity}")
    print(f"Initial sold_out status: {product.sold_out}")
    
    # Create cart and add items
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Clear any existing cart items
    CartItem.objects.filter(cart=cart).delete()
    
    # Add 2 items to cart
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2
    )
    
    print(f"\\nAdded {cart_item.quantity} items to cart")
    print(f"Cart total: ${cart.total_price}")
    
    # Simulate checkout process
    client = Client()
    
    # Login user
    login_success = client.login(username='testuser', password='testpass123')
    print(f"\\nLogin successful: {login_success}")
    
    if login_success:
        # Test checkout
        checkout_url = reverse('payment:checkout')
        
        checkout_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '12345',
            'payment_method': 'cash_on_delivery'
        }
        
        print(f"\\nSubmitting checkout form...")
        response = client.post(checkout_url, checkout_data)
        
        # Check if order was created
        orders = Order.objects.filter(user=user)
        if orders.exists():
            order = orders.first()
            print(f"✅ Order created successfully!")
            print(f"Order ID: {order.id}")
            print(f"Order total: ${order.total_amount}")
            print(f"Order items count: {order.items.count()}")
            
            # Check if product quantity was decreased
            product.refresh_from_db()
            print(f"\\nProduct quantity after order: {product.quantity}")
            print(f"Product sold_out status: {product.sold_out}")
            
            # Check order items
            for item in order.items.all():
                print(f"Order item: {item.quantity} x {item.product.name} @ ${item.price}")
            
            # Test 2: Try to add more items to cart than available
            print(f"\\n" + "=" * 60)
            print("Test 2: Adding more items than available to cart")
            
            # Clear cart
            CartItem.objects.filter(cart=cart).delete()
            
            # Try to add more items than available (should be limited)
            remaining_qty = product.quantity
            try:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=remaining_qty + 1  # More than available
                )
                print(f"Added {cart_item.quantity} items to cart")
            except Exception as e:
                print(f"Error adding items: {e}")
            
            # Test 3: Complete the remaining stock
            print(f"\\n" + "=" * 60)
            print("Test 3: Order remaining stock to make product sold out")
            
            # Clear cart and add remaining items
            CartItem.objects.filter(cart=cart).delete()
            
            if remaining_qty > 0:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=remaining_qty
                )
                
                # Checkout again
                response = client.post(checkout_url, checkout_data)
                
                # Check final status
                product.refresh_from_db()
                print(f"Final product quantity: {product.quantity}")
                print(f"Final sold_out status: {product.sold_out}")
                print(f"Product is_available(): {product.is_available()}")
                
                if product.sold_out:
                    print("✅ Product is now sold out!")
                else:
                    print("❌ Product should be sold out but isn't")
            
        else:
            print("❌ No order was created")
            print(f"Response status: {response.status_code}")
    else:
        print("❌ Login failed")
    
    print(f"\\n" + "=" * 60)
    print("Checkout with quantity management test completed!")

if __name__ == '__main__':
    test_checkout_with_quantity_management()
