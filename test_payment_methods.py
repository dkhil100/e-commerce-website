#!/usr/bin/env python
"""
Test both payment methods to ensure they work correctly
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Add testserver to ALLOWED_HOSTS for testing
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from store.models import Product, Category
from cart.models import CartItem, Cart
from payment.models import Order, OrderItem, Payment
from django.contrib.auth.models import User

def test_payment_methods():
    """Test both payment methods"""
    print("🧪 Testing both payment methods...")
    
    # Get or create test user
    User = get_user_model()
    try:
        user = User.objects.get(username='testuser')
        print(f"✅ Using existing user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(username='testuser', password='testpass123')
        print(f"✅ Created new user: {user.username}")
    
    # Create a test client and login
    client = Client()
    login_success = client.login(username='testuser', password='testpass123')
    print(f"🔑 Login success: {login_success}")
    
    if not login_success:
        print("❌ Login failed - cannot proceed with checkout test")
        return False
    
    # Test 1: Credit Card Payment
    print("\n💳 Testing Credit Card Payment...")
    
    # Clear and add items to cart
    cart, created = Cart.objects.get_or_create(user=user)
    cart.items.all().delete()
    
    products = Product.objects.all()[:1]
    for product in products:
        CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
    
    checkout_url = reverse('payment:checkout')
    
    credit_card_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'postal_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '4111111111111111',
        'expiry_month': '12',
        'expiry_year': '2025',
        'cvv': '123',
        'card_holder_name': 'Test User'
    }
    
    response = client.post(checkout_url, credit_card_data)
    
    if response.status_code == 302:
        orders = Order.objects.filter(user=user).order_by('-created_at')
        if orders.exists():
            latest_order = orders.first()
            print(f"📦 Credit Card Order #{latest_order.id}")
            print(f"   Payment Status: {latest_order.payment_status}")
            
            if latest_order.payment_status == 'paid':
                print("✅ Credit card payment status is correctly set to 'paid'")
            else:
                print(f"❌ Credit card payment status should be 'paid' but is '{latest_order.payment_status}'")
                return False
    
    # Test 2: Cash on Delivery Payment
    print("\n💰 Testing Cash on Delivery Payment...")
    
    # Clear and add items to cart again
    cart.items.all().delete()
    
    for product in products:
        CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
    
    cod_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'postal_code': '12345',
        'payment_method': 'cash_on_delivery',
    }
    
    response = client.post(checkout_url, cod_data)
    
    if response.status_code == 302:
        orders = Order.objects.filter(user=user).order_by('-created_at')
        if orders.exists():
            latest_order = orders.first()
            print(f"📦 Cash on Delivery Order #{latest_order.id}")
            print(f"   Payment Status: {latest_order.payment_status}")
            
            if latest_order.payment_status == 'pending':
                print("✅ Cash on delivery payment status is correctly set to 'pending'")
            else:
                print(f"❌ Cash on delivery payment status should be 'pending' but is '{latest_order.payment_status}'")
                return False
    
    print("✅ Both payment methods work correctly!")
    return True

if __name__ == '__main__':
    success = test_payment_methods()
    if success:
        print("\n🎉 All payment methods test passed!")
    else:
        print("\n❌ Payment methods test failed!")
