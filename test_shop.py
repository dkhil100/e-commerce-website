import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from store.models import Product, Category

def test_shop_page():
    client = Client()
    
    # Test the shop page
    response = client.get(reverse('store'))
    print(f"Shop page status: {response.status_code}")
    print(f"Products in context: {len(response.context['products'])}")
    
    # Check if products have images
    for product in response.context['products']:
        print(f"Product: {product.name}")
        print(f"  - Status: {product.status}")
        print(f"  - Image: {product.product_image}")
        print(f"  - Image URL: {product.product_image.url if product.product_image else 'None'}")
        print()
    
    return response

if __name__ == '__main__':
    test_shop_page()
