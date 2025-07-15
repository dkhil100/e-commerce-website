from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session or not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        self.cart[product_id] = quantity  # Always update quantity
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        return {k: int(v) for k, v in self.cart.items()}  # Always return int quantities

    def get_total(self):  # Optional utility method
        total = 0
        products = self.get_prods()
        quantities = self.get_quants()
        for product in products:
            qty = quantities.get(str(product.id), 1)
            total += qty * product.selling_price
        return total
