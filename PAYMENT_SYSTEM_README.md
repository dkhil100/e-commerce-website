# Payment System Documentation

## Overview

The payment system is a comprehensive Django app that handles checkout, orders, and payments for the e-commerce store. It integrates seamlessly with the existing cart and store apps.

## Features

### 1. Checkout Process
- User authentication required
- Customer information collection (name, email, phone)
- Shipping address collection
- Multiple payment methods support:
  - Credit Card
  - Debit Card
  - PayPal
  - Bank Transfer
  - Cash on Delivery

### 2. Order Management
- Complete order tracking from creation to delivery
- Order statuses: Pending, Confirmed, Processing, Shipped, Delivered, Cancelled
- Payment statuses: Pending, Paid, Failed, Refunded
- Order history for users

### 3. Payment Processing
- Secure payment form with validation
- Card details collection (demonstration only - use proper payment gateways in production)
- Transaction ID generation
- Payment success/failure handling

### 4. Admin Interface
- Full order management in Django admin
- Order item inline editing
- Payment information tracking
- Customer and shipping details

## URL Structure

- `/payment/checkout/` - Checkout page
- `/payment/process/` - Payment processing endpoint
- `/payment/success/<order_id>/` - Payment success page
- `/payment/failed/` - Payment failure page
- `/payment/orders/` - Order history
- `/payment/order/<order_id>/` - Order detail view

## Models

### Order
- User information and shipping details
- Payment and order status tracking
- Total amount calculation
- Created/updated timestamps

### OrderItem
- Links orders to products
- Quantity and price at time of order
- Total price calculation

### Payment
- Payment method and amount
- Transaction ID
- Card details (masked for security)
- Payment timestamp

## Templates

### Checkout (`checkout.html`)
- Three-section layout: Customer info, Shipping address, Payment method
- Dynamic card form based on payment method
- Responsive design with Bootstrap 5
- Real-time form validation

### Payment Success (`payment_success.html`)
- Order confirmation details
- Order items summary
- Next steps information
- Links to order history and continue shopping

### Payment Failed (`payment_failed.html`)
- Error message and troubleshooting tips
- Options to retry or contact support
- Links back to checkout and cart

### Order History (`order_history.html`)
- Grid layout of user's orders
- Order status badges
- Quick access to order details

### Order Detail (`order_detail.html`)
- Complete order information
- Order timeline with status progression
- Customer and shipping information
- Payment details

## Integration Points

### Cart Integration
- Reads cart contents from session
- Converts cart items to order items
- Clears cart after successful payment

### Store Integration
- Links to product models
- Uses product pricing information
- Maintains product inventory references

### User Authentication
- Requires login for checkout
- Pre-fills user information
- Maintains order history per user

## Security Features

1. **CSRF Protection** - All forms include CSRF tokens
2. **Authentication Required** - All views require user login
3. **Input Validation** - Forms validate all user inputs
4. **Card Number Masking** - Only last 4 digits stored
5. **Transaction Security** - Unique transaction IDs

## Usage Instructions

### For Customers
1. Add items to cart
2. Go to cart and click "Valider la commande" (Checkout)
3. Fill in customer information
4. Enter shipping address
5. Select payment method and enter details
6. Review order and click "Place Order"
7. View confirmation or handle payment failure

### For Administrators
1. Access Django admin at `/admin/`
2. Navigate to Payment section
3. View and manage orders, order items, and payments
4. Update order statuses as needed
5. Process refunds or cancellations

## Testing

The payment system includes comprehensive tests:
- Model tests for Order, OrderItem, and Payment
- View tests for all payment endpoints
- Authentication and authorization tests
- Template rendering tests

Run tests with:
```bash
python manage.py test payment
```

## Production Considerations

**Important**: This is a demonstration payment system. For production use:

1. **Payment Gateway Integration**: Replace the simulation with real payment processors like Stripe, PayPal, or Square
2. **SSL/TLS**: Ensure all payment pages use HTTPS
3. **PCI Compliance**: Never store actual card numbers or CVV codes
4. **Security Audits**: Regular security reviews and penetration testing
5. **Logging**: Implement comprehensive payment logging
6. **Backup**: Regular database backups for order data
7. **Monitoring**: Monitor payment success/failure rates

## Customization

### Adding New Payment Methods
1. Update `PAYMENT_METHOD_CHOICES` in `models.py`
2. Add form fields in `forms.py`
3. Update template to show/hide relevant fields
4. Modify payment processing logic in `views.py`

### Styling
- Templates use Bootstrap 5 for responsive design
- Custom CSS included for enhanced animations
- Easy to integrate with existing site themes

### Email Notifications
Consider adding email notifications for:
- Order confirmation
- Payment success/failure
- Shipping updates
- Delivery confirmation

## Support

For issues or questions about the payment system:
1. Check the Django logs for error messages
2. Review the test cases for expected behavior
3. Verify database migrations are applied
4. Ensure all required dependencies are installed

The payment system is designed to be robust, secure, and user-friendly while maintaining compatibility with the existing store architecture.
