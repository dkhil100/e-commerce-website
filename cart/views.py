from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from store.models import Product
from django.http import JsonResponse
from django.db.models import Sum

def get_or_create_cart(user):
    """Get or create a cart for the user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def cart_summary(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    cart_total = cart.total_price
    total_orders = cart.total_orders
    
    return render(request, 'cart_summary.html', {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "total_orders": total_orders
    })

@login_required
def cart_add(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty', 1))
        
        # Ensure quantity is within limits (1-5)
        if product_qty < 1:
            product_qty = 1
        elif product_qty > 5:
            product_qty = 5
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is sold out or not available
        if product.sold_out or product.quantity <= 0:
            return JsonResponse({'success': False, 'error': 'Product is sold out'})
        
        # Check if requested quantity is available
        if product_qty > product.quantity:
            return JsonResponse({'success': False, 'error': f'Only {product.quantity} items available'})
        
        cart = get_or_create_cart(request.user)
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': product_qty}
        )
        
        if not created:
            # Check if total quantity (existing + new) exceeds available stock
            total_qty = product_qty
            if total_qty > product.quantity:
                return JsonResponse({'success': False, 'error': f'Only {product.quantity} items available'})
            
            # Replace quantity instead of adding (as per user request)
            cart_item.quantity = product_qty
            cart_item.save()
        
        cart_quantity = cart.total_orders
        messages.success(request, f'{product.name} added to cart!')
        
        return JsonResponse({'qty': cart_quantity, 'success': True})
    
    return JsonResponse({'success': False}, status=400)

@login_required
def cart_delete(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = get_or_create_cart(request.user)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            product_name = cart_item.product.name
            cart_item.delete()
            messages.success(request, f'{product_name} removed from cart!')
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
    
    return JsonResponse({'success': False}, status=400)

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request.user)
        
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    qty = int(value)
                    # Enforce quantity limits
                    if qty < 1:
                        qty = 1
                    elif qty > 5:
                        qty = 5
                    
                    if qty > 0:
                        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
                        
                        # Check if product is still available
                        if cart_item.product.sold_out or cart_item.product.quantity <= 0:
                            messages.error(request, f'{cart_item.product.name} is sold out and has been removed from cart.')
                            cart_item.delete()
                            continue
                        
                        # Check if requested quantity is available
                        if qty > cart_item.product.quantity:
                            qty = cart_item.product.quantity
                            messages.warning(request, f'Only {qty} items available for {cart_item.product.name}')
                        
                        cart_item.quantity = qty
                        cart_item.save()
                    else:
                        # Remove item if quantity is 0
                        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
                except (ValueError, CartItem.DoesNotExist):
                    pass
        
        messages.success(request, 'Cart updated successfully!')
        return redirect('cart_summary')
    
    return redirect('cart_summary')

# Function to get cart count for templates
def get_cart_count(user):
    """Helper function to get cart count for a user"""
    if user.is_authenticated:
        cart = get_or_create_cart(user)
        return cart.total_orders
    return 0