from django.contrib import admin
from django import forms
from .models import Order, OrderItem, Payment


class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for new items
        if not self.instance.pk:
            self.fields['quantity'].initial = 1
            self.fields['price'].initial = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInlineForm
    extra = 0
    readonly_fields = ('get_total_price_display',)
    fields = ('product', 'quantity', 'price', 'get_total_price_display')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'email', 'total_amount', 'payment_status', 'order_status', 'created_at']
    list_filter = ['payment_status', 'order_status', 'created_at']
    search_fields = ['user__username', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'total_amount', 'payment_status', 'order_status')
        }),
        ('Customer Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total_price_display']
    list_filter = ['order__created_at']
    search_fields = ['product__name', 'order__user__username']
    
    def get_total_price_display(self, obj):
        return obj.get_total_price_display()
    get_total_price_display.short_description = 'Total Price'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'amount', 'transaction_id', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['order__user__username', 'transaction_id']
    readonly_fields = ['created_at']
