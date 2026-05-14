from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def order_number(self):
        """
        Get the sequential order number for this order.
        This will automatically adjust when orders are deleted.
        """
        # Get all orders for this user, ordered by creation date
        user_orders = Order.objects.filter(user=self.user).order_by('created_at')
        
        # Find the position of this order in the sequence
        for index, order in enumerate(user_orders, 1):
            if order.id == self.id:
                return index
        
        # Fallback to database ID if not found
        return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        if self.product and self.quantity:
            return f"{self.quantity} x {self.product.name}"
        return "OrderItem (incomplete)"
    
    @property
    def total_price(self):
        if self.quantity is not None and self.price is not None:
            return self.quantity * self.price
        return 0
    
    def get_total_price_display(self):
        """Admin-friendly display of total price"""
        if self.quantity is not None and self.price is not None:
            return f"${self.quantity * self.price:.2f}"
        return "N/A"

    def save(self, *args, **kwargs):
        if self.pk is None and self.quantity is not None and self.product is not None:  # Only decrease quantity on creation
            self.product.quantity -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Card details (for demonstration - in production, use proper payment gateways)
    card_number = models.CharField(max_length=19, blank=True, null=True)  # Masked card number
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order {self.order.id}"
