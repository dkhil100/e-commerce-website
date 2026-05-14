#!/usr/bin/env python
"""
Test Cash on Delivery payment method
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

def test_cash_on_delivery():
    """Test Cash on Delivery payment method"""
    print("🧪 Testing Cash on Delivery payment method...")
    
    # Get or create test user
    User = get_user_model()
    try:
        user = User.objects.get(username='testuser')
        print(f"✅ Using existing user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(username='testuser', password='testpass123')
        print(f"✅ Created new user: {user.username}")
    
    # Clear any existing cart items for this user
    cart, created = Cart.objects.get_or_create(user=user)
    cart.items.all().delete()  # Clear cart first
    
    # Add some test items to cart
    print("🛒 Adding test items to cart...")
    try:
        products = Product.objects.all()[:1]  # Just one item for testing
        for product in products:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 1}
            )
            print(f"   Added {product.name} to cart")
    except Exception as e:
        print(f"❌ Error adding items to cart: {e}")
        return False
    
    # Create a test client and login
    client = Client()
    login_success = client.login(username='testuser', password='testpass123')
    print(f"🔑 Login success: {login_success}")
    
    if not login_success:
        print("❌ Login failed - cannot proceed with checkout test")
        return False
    
    # Test cash on delivery checkout
    try:
        print("💰 Testing Cash on Delivery checkout...")
        
        checkout_url = reverse('payment:checkout')
        
        checkout_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '12345',
            'payment_method': 'cash_on_delivery',
            # No card details needed for cash on delivery
        }
        
        response = client.post(checkout_url, checkout_data)
        print(f"💰 Checkout submission response: {response.status_code}")
        
        if response.status_code == 302:  # Redirect to success page
            print("✅ Checkout successful - redirected to success page")
            
            # Check if order was created
            orders = Order.objects.filter(user=user).order_by('-created_at')
            if orders.exists():
                latest_order = orders.first()
                print(f"📦 Order created: #{latest_order.id}")
                print(f"   Payment Status: {latest_order.payment_status}")
                print(f"   Order Status: {latest_order.order_status}")
                print(f"   Total: ${latest_order.total_amount}")
                
                # Check if payment status is pending for cash on delivery
                if latest_order.payment_status == 'pending':
                    print("✅ Payment status is correctly set to 'pending' for cash on delivery")
                else:
                    print(f"❌ Payment status should be 'pending' but is '{latest_order.payment_status}'")
                    return False
                
                # Check if payment was created
                payments = Payment.objects.filter(order=latest_order)
                if payments.exists():
                    payment = payments.first()
                    print(f"💰 Payment created: {payment.payment_method}")
                    print(f"   Amount: ${payment.amount}")
                    if payment.payment_method == 'cash_on_delivery':
                        print("✅ Payment method correctly set to 'cash_on_delivery'")
                    else:
                        print(f"❌ Payment method should be 'cash_on_delivery' but is '{payment.payment_method}'")
                        return False
                else:
                    print("❌ No payment record found")
                    return False
            else:
                print("❌ No order was created")
                return False
                
        else:
            print(f"❌ Checkout failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during checkout: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("✅ Cash on Delivery test passed!")
    return True

if __name__ == '__main__':
    success = test_cash_on_delivery()
    if success:
        print("\n🎉 Cash on Delivery test passed! Payment status is correctly set to 'pending'.")
    else:
        print("\n❌ Cash on Delivery test failed!")
