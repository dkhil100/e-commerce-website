#!/usr/bin/env python
"""
Full checkout test - Tests the complete checkout workflow including cart clearing
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

def test_complete_checkout_flow():
    """Test the complete checkout workflow"""
    print("🧪 Testing complete checkout workflow...")
    
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
    initial_cart_count = cart.items.count()
    print(f"📦 Initial cart items: {initial_cart_count}")
    
    if initial_cart_count == 0:
        # Add some test items to cart
        print("🛒 Adding test items to cart...")
        try:
            # Get some products
            products = Product.objects.all()[:2]
            for product in products:
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': 1}
                )
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                print(f"   Added {product.name} to cart")
        except Exception as e:
            print(f"❌ Error adding items to cart: {e}")
            return False
    
    # Check cart before checkout
    cart_items_before = cart.items.count()
    total_before = sum(item.product.selling_price * item.quantity for item in cart.items.all())
    print(f"🛒 Cart before checkout: {cart_items_before} items, total: ${total_before}")
    
    # Create a test client and login
    client = Client()
    login_success = client.login(username='testuser', password='testpass123')
    print(f"🔑 Login success: {login_success}")
    
    if not login_success:
        print("❌ Login failed - cannot proceed with checkout test")
        return False
    
    # Get checkout page
    try:
        checkout_url = reverse('payment:checkout')
        print(f"📄 Accessing checkout page: {checkout_url}")
        
        response = client.get(checkout_url)
        print(f"📄 Checkout page response: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Checkout page not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing checkout page: {e}")
        return False
    
    # Test checkout submission
    try:
        print("💳 Testing checkout submission...")
        
        checkout_data = {
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
        
        response = client.post(checkout_url, checkout_data)
        print(f"💳 Checkout submission response: {response.status_code}")
        
        if response.status_code == 302:  # Redirect to success page
            print("✅ Checkout successful - redirected to success page")
            
            # Check if cart was cleared
            cart_items_after = cart.items.count()
            print(f"🛒 Cart after checkout: {cart_items_after} items")
            
            if cart_items_after == 0:
                print("✅ Cart was successfully cleared after checkout")
            else:
                print("❌ Cart was not cleared after checkout")
                return False
            
            # Check if order was created
            orders = Order.objects.filter(user=user).order_by('-created_at')
            if orders.exists():
                latest_order = orders.first()
                print(f"📦 Order created: #{latest_order.id}")
                print(f"   Status: {latest_order.order_status}")
                print(f"   Payment Status: {latest_order.payment_status}")
                print(f"   Total: ${latest_order.total_amount}")
                print(f"   Items: {latest_order.items.count()}")
                
                # Check if payment was created
                payments = Payment.objects.filter(order=latest_order)
                if payments.exists():
                    payment = payments.first()
                    print(f"💰 Payment created: {payment.payment_method}")
                    print(f"   Amount: ${payment.amount}")
                    print(f"   Transaction ID: {payment.transaction_id}")
                else:
                    print("❌ No payment record found")
                    return False
            else:
                print("❌ No order was created")
                return False
                
        else:
            print(f"❌ Checkout failed with status: {response.status_code}")
            if hasattr(response, 'context') and response.context:
                if 'form' in response.context:
                    form = response.context['form']
                    if form.errors:
                        print(f"Form errors: {form.errors}")
                if 'payment_form' in response.context:
                    payment_form = response.context['payment_form']
                    if payment_form.errors:
                        print(f"Payment form errors: {payment_form.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error during checkout: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("✅ Complete checkout flow test passed!")
    return True

if __name__ == '__main__':
    success = test_complete_checkout_flow()
    if success:
        print("\n🎉 All tests passed! Checkout system is working correctly.")
    else:
        print("\n❌ Tests failed! There are issues with the checkout system.")
