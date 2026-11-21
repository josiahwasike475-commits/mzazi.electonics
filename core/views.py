import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from catalog.views import catalogue_context
from .assistant import answer


def home(request):
    context = catalogue_context(page_title="Quality electronics for everyday life", active_nav="home")
    context["categories"] = [category for category in context["categories"] if category["slug"] not in {"networking-security", "bulbs"}]
    return render(request, "home.html", context)


def about(request):
    return render(request, "simple_page.html", {"page_title": "About Mzazi Electronics", "simple_page": "about", "active_nav": "about"})


def contact(request):
    return render(request, "simple_page.html", {"page_title": "Talk to Mzazi Electronics", "simple_page": "contact", "active_nav": "contact"})


def newsletter(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "Use POST to subscribe."}, status=405)
    return JsonResponse({"ok": True, "message": "You’re on the list. We’ll only send useful updates."})


@csrf_exempt
def assistant_api(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "Use POST to chat with Mza AI."}, status=405)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}
    message = str(payload.get("message", "")).strip()
    history = payload.get("history", [])
    if not isinstance(history, list):
        history = []
    return JsonResponse({"ok": True, "reply": answer(message, history)})


def routes_manifest(request):
    return JsonResponse({"routes": [
        {"path": "/", "title": "Home"},
        {"path": "/shop/", "title": "Shop"},
        {"path": "/category/:slug/", "title": "Category"},
        {"path": "/product/:slug/", "title": "Product details"},
        {"path": "/cart/", "title": "Cart"},
        {"path": "/checkout/", "title": "Checkout"},
        {"path": "/about/", "title": "About Mzazi Electronics"},
        {"path": "/contact/", "title": "Contact Mzazi Electronics"},
        {"path": "/account/", "title": "Account"},
        {"path": "/account/register/", "title": "Create account"},
        {"path": "/order/:order_number/", "title": "Order status"},
        {"path": "/dashboard/", "title": "Shop management"},
        {"path": "/admin-panel/", "title": "Admin control room"},
        {"path": "/simple-admin/", "title": "Simple Admin"},
        {"path": "/simple-admin/product/add/", "title": "Add product"},
        {"path": "/simple-admin/category/add/", "title": "Add category"},
        {"path": "/simple-admin/brand/add/", "title": "Add brand"},
    ]})
