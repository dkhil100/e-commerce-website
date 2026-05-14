#!/usr/bin/env python
"""
Check orders and cart status
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
from payment.models import Order, OrderItem, Payment

def check_status():
    """Check current status of orders and cart"""
    print("📊 Checking current status...")
    
    # Get test user
    try:
        user = User.objects.get(username='testuser')
        print(f"✅ Found user: {user.username}")
    except User.DoesNotExist:
        print("❌ Test user not found")
        return
    
    # Check cart
    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.count()
        print(f"🛒 Cart items: {cart_items}")
        if cart_items > 0:
            print(f"   Total price: ${cart.total_price}")
            for item in cart.items.all():
                print(f"   - {item.product.name} (qty: {item.quantity})")
        else:
            print("   Cart is empty")
    except Cart.DoesNotExist:
        print("❌ Cart not found")
    
    # Check orders
    orders = Order.objects.filter(user=user).order_by('-created_at')
    print(f"\n📦 Orders: {orders.count()}")
    
    for order in orders:
        print(f"\n   Order #{order.id}:")
        print(f"   - Date: {order.created_at}")
        print(f"   - Status: {order.order_status}")
        print(f"   - Payment: {order.payment_status}")
        print(f"   - Total: ${order.total_amount}")
        print(f"   - Items: {order.items.count()}")
        
        for item in order.items.all():
            print(f"     • {item.product.name} (qty: {item.quantity}) - ${item.total_price}")
        
        # Check payment
        if hasattr(order, 'payment'):
            payment = order.payment
            print(f"   - Payment method: {payment.payment_method}")
            print(f"   - Transaction ID: {payment.transaction_id}")
    
    if orders.count() == 0:
        print("   No orders found")

if __name__ == '__main__':
    check_status()
