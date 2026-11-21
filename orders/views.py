import json
import os
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from catalog.models import Product
from catalog.views import catalogue_context
from .models import Order, OrderItem
from .mpesa import MpesaConfigurationError, initiate_stk_push, process_callback


def cart(request):
    return render(request, "cart.html", catalogue_context(page_title="Your cart", active_nav="cart"))


def checkout(request):
    return render(request, "checkout.html", catalogue_context(page_title="Checkout", active_nav="cart"))


def order_status(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "order_status.html", {"page_title": f"Order {order.order_number}", "order": order, "active_nav": "cart"})


def _body(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _money(value):
    return Decimal(str(value or 0))


@require_POST
def create_order(request):
    body = _body(request)
    customer = body.get("customer") or {}
    items = body.get("items") or []
    if not customer.get("name") or not customer.get("phone") or not customer.get("location") or not items:
        return JsonResponse({"ok": False, "message": "Please provide your name, phone, delivery location and at least one item."}, status=400)

    idempotency_key = body.get("idempotency_key") or ""
    if idempotency_key:
        existing = Order.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return JsonResponse({"ok": True, "order_number": existing.order_number, "status_url": f"/order/{existing.order_number}/", "duplicate": True})

    product_ids = [item.get("id") for item in items]
    products = {product.id: product for product in Product.objects.filter(id__in=product_ids, is_active=True)}
    if len(products) != len(set(product_ids)):
        return JsonResponse({"ok": False, "message": "One or more products are no longer available."}, status=400)

    subtotal = Decimal("0")
    with transaction.atomic():
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            customer_name=str(customer.get("name", "")).strip(),
            phone=str(customer.get("phone", "")).strip(),
            email=str(customer.get("email", "")).strip(),
            delivery_location=str(customer.get("location", "")).strip(),
            instructions=str(customer.get("instructions", "")).strip(),
            delivery_fee=_money(os.getenv("DEFAULT_DELIVERY_FEE", getattr(settings, "DEFAULT_DELIVERY_FEE", "0"))),
            payment_method=body.get("payment_method", "whatsapp"),
            idempotency_key=idempotency_key,
        )
        for item in items:
            product = products[int(item["id"])]
            quantity = max(1, min(int(item.get("quantity", 1)), 20))
            unit_price = product.price
            if unit_price is not None:
                subtotal += unit_price * quantity
            OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=unit_price, quantity=quantity)
        order.subtotal = subtotal
        order.total = subtotal + order.delivery_fee
        order.save(update_fields=["subtotal", "total", "updated_at"])

    return JsonResponse({
        "ok": True,
        "order_number": order.order_number,
        "status_url": f"/order/{order.order_number}/",
        "whatsapp_url": f"https://wa.me/254786163265?text=Hello%20Josiah%2C%20I%27d%20like%20help%20with%20order%20{order.order_number}.",
        "payment_status": order.payment_status,
        "total": float(order.total),
    })


@require_POST
def stk_push(request):
    body = _body(request)
    order_number = body.get("order_number")
    phone = str(body.get("phone", "")).strip()
    order = get_object_or_404(Order, order_number=order_number)
    if order.payment_method != "mpesa":
        return JsonResponse({"ok": False, "message": "This order was not created for M-Pesa."}, status=400)
    if order.total <= 0:
        return JsonResponse({"ok": False, "message": "This order has no configured payable total yet. Ask the shop to confirm pricing on WhatsApp."}, status=400)
    try:
        attempt, result = initiate_stk_push(order, phone)
    except MpesaConfigurationError as exc:
        return JsonResponse({"ok": False, "configured": False, "message": str(exc)}, status=503)
    except Exception:
        return JsonResponse({"ok": False, "configured": True, "message": "Safaricom could not accept the request. Please try again or use WhatsApp."}, status=502)
    return JsonResponse({"ok": True, "configured": True, "status": attempt.status, "message": result.get("CustomerMessage", "Check your phone for the M-Pesa prompt."), "checkout_request_id": attempt.checkout_request_id})


@csrf_exempt
@require_POST
def mpesa_callback(request):
    payload = _body(request)
    processed = process_callback(payload)
    return JsonResponse({"ResultCode": 0 if processed else 1, "ResultDesc": "Accepted" if processed else "Unknown checkout request"})
