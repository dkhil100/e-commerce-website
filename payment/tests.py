from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Order, OrderItem, Payment
from store.models import Product, Category


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            meta_title='Test Category',
            meta_keywords='test, category',
            meta_description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            small_description='A test product',
            description='This is a test product',
            quantity=10,
            original_price=29.99,
            selling_price=19.99,
            tag='test',
            meta_title='Test Product',
            meta_keywords='test, product',
            meta_description='Test product description',
            category=self.category
        )
        
    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            total_amount=Decimal('19.99')
        )
        
        self.assertEqual(order.full_name, 'John Doe')
        self.assertEqual(order.payment_status, 'pending')
        self.assertEqual(order.order_status, 'pending')
        
    def test_order_item_creation(self):
        order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            total_amount=Decimal('19.99')
        )
        
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=Decimal('19.99')
        )
        
        self.assertEqual(order_item.total_price, Decimal('39.98'))
        
    def test_payment_creation(self):
        order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            total_amount=Decimal('19.99')
        )
        
        payment = Payment.objects.create(
            order=order,
            payment_method='credit_card',
            amount=Decimal('19.99'),
            transaction_id='test_txn_123'
        )
        
        self.assertEqual(payment.order, order)
        self.assertEqual(payment.payment_method, 'credit_card')


class PaymentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            meta_title='Test Category',
            meta_keywords='test, category',
            meta_description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            small_description='A test product',
            description='This is a test product',
            quantity=10,
            original_price=29.99,
            selling_price=19.99,
            tag='test',
            meta_title='Test Product',
            meta_keywords='test, product',
            meta_description='Test product description',
            category=self.category
        )
        
    def test_checkout_view_requires_login(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_checkout_view_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('checkout'))
        # Will redirect to cart_summary if cart is empty
        self.assertEqual(response.status_code, 302)
        
    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order History')
        
    def test_payment_success_view(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Create an order first
        order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            total_amount=Decimal('19.99')
        )
        
        response = self.client.get(reverse('payment_success', kwargs={'order_id': order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment Successful')
        
    def test_payment_failed_view(self):
        response = self.client.get(reverse('payment_failed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment Failed')
