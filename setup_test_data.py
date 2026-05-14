#!/usr/bin/env python
"""
Manual checkout test script
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

def setup_test_data():
    """Set up test data for checkout"""
    print("🛒 Setting up test data for checkout...")
    
    # Create/get test user
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
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Found existing user: {user.username}")
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=user)
    if created:
        print("✅ Created new cart")
    else:
        print("✅ Found existing cart")
    
    # Clear existing cart items
    cart.items.all().delete()
    print("✅ Cleared existing cart items")
    
    # Get products
    products = Product.objects.all()[:2]
    if not products:
        print("❌ No products found. Please add some products first.")
        return False
    
    # Add products to cart
    for product in products:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        print(f"✅ Added {product.name} to cart")
    
    print(f"✅ Cart now has {cart.total_items} items worth ${cart.total_price}")
    print("\n🎯 Test data setup complete!")
    print("\nNow you can:")
    print("1. Go to http://127.0.0.1:8000/")
    print("2. Login with username: testuser, password: testpass123")
    print("3. Go to cart and proceed to checkout")
    print("4. Fill out the form and click 'Place Order'")
    print("5. Check if items disappear from cart and order is created")
    
    return True

if __name__ == '__main__':
    setup_test_data()
