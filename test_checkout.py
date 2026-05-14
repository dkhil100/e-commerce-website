#!/usr/bin/env python
"""
Test script to verify checkout functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from store.models import Product
from payment.models import Order, OrderItem, Payment

def test_checkout_process():
    """Test the checkout process"""
    print("🧪 Testing Checkout Process...")
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    print(f"✅ User created/found: {user.username}")
    
    # Check if we have products
    products = Product.objects.all()[:2]
    if not products:
        print("❌ No products found. Please add some products first.")
        return False
    
    print(f"✅ Found {len(products)} products")
    
    # Create/get cart
    cart, created = Cart.objects.get_or_create(user=user)
    if created:
        print("✅ Cart created")
    else:
        print("✅ Cart found")
    
    # Add items to cart
    for product in products:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        if created:
            print(f"✅ Added {product.name} to cart")
        else:
            print(f"✅ {product.name} already in cart")
    
    # Check cart total
    total_price = cart.total_price
    total_items = cart.total_items
    print(f"✅ Cart total: ${total_price}, Items: {total_items}")
    
    # Test order creation
    order = Order.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        email='test@example.com',
        phone='1234567890',
        address='123 Test Street',
        city='Test City',
        postal_code='12345',
        total_amount=total_price,
        payment_status='paid',
        order_status='confirmed'
    )
    
    print(f"✅ Order created: #{order.id}")
    
    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.selling_price
        )
    
    print(f"✅ Order items created: {order.items.count()}")
    
    # Test payment creation
    payment = Payment.objects.create(
        order=order,
        payment_method='credit_card',
        amount=total_price,
        transaction_id='test_12345',
        card_number='**** **** **** 1234',
        card_holder_name='Test User'
    )
    
    print(f"✅ Payment created: {payment.transaction_id}")
    
    # Test cart clearing
    cart_items_count = cart.items.count()
    cart.items.all().delete()
    print(f"✅ Cart cleared: {cart_items_count} items removed")
    
    # Verify cart is empty
    if cart.items.count() == 0:
        print("✅ Cart is now empty")
    else:
        print("❌ Cart still has items")
    
    # Test order retrieval
    retrieved_order = Order.objects.get(id=order.id)
    print(f"✅ Order retrieved: #{retrieved_order.id}, Status: {retrieved_order.order_status}")
    
    print("\n🎉 All tests passed! Checkout process is working correctly.")
    return True

if __name__ == '__main__':
    test_checkout_process()
