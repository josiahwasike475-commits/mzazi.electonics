from django.contrib import admin
from .models import Order, OrderItem, PaymentAttempt


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "unit_price", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "customer_name", "total", "status", "payment_status", "created_at"]
    list_filter = ["status", "payment_status", "payment_method", "created_at"]
    search_fields = ["order_number", "customer_name", "phone", "mpesa_receipt"]
    inlines = [OrderItemInline]
    readonly_fields = ["order_number", "subtotal", "total", "created_at", "updated_at"]


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ["order", "phone", "amount", "status", "mpesa_receipt", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["checkout_request_id", "mpesa_receipt", "order__order_number"]
    readonly_fields = ["raw_callback"]
