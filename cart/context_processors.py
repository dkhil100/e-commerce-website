from .models import Cart

def cart(request):
    """Context processor to make cart available in all templates"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart': cart.items.all(), 'cart_count': cart.total_orders}
        except Cart.DoesNotExist:
            return {'cart': [], 'cart_count': 0}
    return {'cart': [], 'cart_count': 0}