from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart, CartItem
from .models import Order, OrderItem, Payment
from .forms import CheckoutForm, PaymentForm
import uuid
from decimal import Decimal


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    if not cart or cart_items.count() == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_summary')
    
    if request.method == 'POST':
        checkout_form = CheckoutForm(request.POST)
        payment_form = PaymentForm(request.POST)
        
        if checkout_form.is_valid() and payment_form.is_valid():
            try:
                with transaction.atomic():
                    # Validate product availability before creating order
                    for cart_item in cart_items:
                        if cart_item.product.sold_out or cart_item.product.quantity <= 0:
                            messages.error(request, f'{cart_item.product.name} is sold out.')
                            return redirect('payment:checkout')
                        
                        if cart_item.quantity > cart_item.product.quantity:
                            messages.error(request, f'Only {cart_item.product.quantity} items available for {cart_item.product.name}.')
                            return redirect('payment:checkout')
                    
                    # Create order
                    order = checkout_form.save(commit=False)
                    order.user = request.user
                    order.total_amount = cart.total_price
                    order.save()
                    
                    # Create order items
                    for cart_item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.selling_price
                        )
                    
                    # Process payment
                    payment = payment_form.save(commit=False)
                    payment.order = order
                    payment.amount = order.total_amount
                    payment.transaction_id = str(uuid.uuid4())
                    
                    # Handle card details for card payments
                    if payment.payment_method in ['credit_card', 'debit_card']:
                        card_number = payment_form.cleaned_data.get('card_number', '')
                        # Mask card number (keep last 4 digits)
                        if len(card_number) >= 4:
                            payment.card_number = '*' * (len(card_number) - 4) + card_number[-4:]
                        else:
                            payment.card_number = card_number
                        payment.card_holder_name = payment_form.cleaned_data.get('card_holder_name', '')
                    
                    payment.save()
                    
                    # Simulate payment processing
                    if simulate_payment_processing(payment):
                        # For cash on delivery, payment status should remain pending
                        if payment.payment_method == 'cash_on_delivery':
                            order.payment_status = 'pending'
                        else:
                            order.payment_status = 'paid'
                        
                        order.order_status = 'confirmed'
                        order.save()
                        
                        # Clear cart - Make sure we delete all items
                        cart.items.all().delete()
                        
                        if payment.payment_method == 'cash_on_delivery':
                            messages.success(request, 'Order confirmed! You will pay upon delivery.')
                        else:
                            messages.success(request, 'Payment successful! Your order has been confirmed.')
                        return redirect('payment:payment_success', order_id=order.id)
                    else:
                        order.payment_status = 'failed'
                        order.save()
                        messages.error(request, 'Payment failed. Please try again.')
                        return redirect('payment:payment_failed')
                        
            except Exception as e:
                print(f"Error processing order: {str(e)}")  # Debug print
                messages.error(request, f'An error occurred while processing your order: {str(e)}')
                return redirect('payment:checkout')
        else:
            # Print form errors for debugging
            print(f"Checkout form errors: {checkout_form.errors}")
            print(f"Payment form errors: {payment_form.errors}")
            messages.error(request, 'Please correct the errors in the form and try again.')
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if request.user.first_name:
            initial_data['first_name'] = request.user.first_name
        if request.user.last_name:
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email
            
        checkout_form = CheckoutForm(initial=initial_data)
        payment_form = PaymentForm()
    
    context = {
        'cart': cart_items,
        'checkout_form': checkout_form,
        'payment_form': payment_form,
        'total_price': cart.total_price,
    }
    return render(request, 'payment/checkout.html', context)


def simulate_payment_processing(payment):
    """
    Simulate payment processing.
    In a real application, this would integrate with payment gateways like Stripe, PayPal, etc.
    """
    # For demonstration, we'll simulate success for most payments
    # In reality, this would make API calls to payment processors
    
    if payment.payment_method == 'cash_on_delivery':
        return True
    
    # Simulate card payment processing
    if payment.payment_method in ['credit_card', 'debit_card']:
        # Simulate some basic validation
        if payment.card_number and len(payment.card_number.replace('*', '').replace(' ', '')) >= 4:
            return True
        return False
    
    # Other payment methods (paypal, bank_transfer) - simulate success
    if payment.payment_method in ['paypal', 'bank_transfer']:
        return True
    
    # Default to success for any other payment method
    return True


@login_required
def process_payment(request):
    """
    Alternative payment processing endpoint if needed
    """
    if request.method == 'POST':
        # Handle AJAX payment processing if needed
        pass
    return redirect('payment:checkout')


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'payment/payment_success.html', context)


def payment_failed(request):
    return render(request, 'payment/payment_failed.html')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'payment/order_history.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'payment/order_detail.html', context)
