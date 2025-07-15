from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    qty_range = range(1, 6)

    cart_total = 0
    # Attach quantity and line_total to each product
    for product in cart_products:
        qty = quantities.get(str(product.id), 1)
        product.qty = qty
        product.line_total = product.selling_price * qty
        cart_total += product.line_total

    return render(request, 'cart_summary.html', {
        "cart_products": cart_products,
        "qty_range": qty_range,
        "cart_total": cart_total
    })


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) 
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

        return response
def cart_delete(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        if product_id and str(product_id) in cart.cart:
            cart.cart.pop(str(product_id), None)
            request.session.modified = True
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def update_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    qty = int(value)
                    product = Product.objects.get(id=product_id)
                    cart.add(product, qty)  # This updates the session
                except (ValueError, Product.DoesNotExist):
                    pass
        return redirect('cart_summary')
    return redirect('cart_summary')