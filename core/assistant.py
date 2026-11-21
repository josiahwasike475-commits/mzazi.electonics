import json
import os
import urllib.error
import urllib.request

from catalog.models import Product

MODEL = "gemini-3.8-flash"

GREETING_REPLY = "hello, karibu sana! mzazi electronics"


def _is_greeting(message):
    normalized = " ".join(str(message or "").lower().strip().replace("!", " ").replace(",", " ").split())
    greetings = {
        "hi", "hello", "hey", "habari", "niaje", "mambo", "jambo", "sasa",
        "good morning", "good afternoon", "good evening", "hello there", "hi there",
    }
    return normalized in greetings


def _catalogue_context():
    products = Product.objects.filter(is_active=True).select_related("brand", "category")
    lines = []
    for product in products[:40]:
        price = f"KSh {product.price:,.0f}" if product.price is not None else "price on request"
        stock = "in stock" if product.stock_quantity > 0 else "availability to confirm"
        lines.append(f"- {product.name} | brand: {product.brand.name if product.brand else 'MZAZI'} | category: {product.category.name} | {price} | {stock} | link: {product.get_absolute_url()}")
    return "\n".join(lines) or "No products are currently listed."


def _fallback():
    return "I’m Mza AI, your Mzazi shopping assistant. I can help you compare categories, find an accessory, or prepare an order. For live price and stock confirmation, chat with Josiah on WhatsApp: https://wa.me/254786163265"


def answer(message, history=None):
    message = str(message or "").strip()[:800]
    if not message:
        return "Tell me what you’re looking for — for example, a phone accessory, Oraimo audio, a laptop, home electronics or networking gear."
    if _is_greeting(message):
        return GREETING_REPLY

    api_url = os.getenv("MANUS_API_URL") or os.getenv("BUILT_IN_FORGE_API_URL")
    api_key = os.getenv("MANUS_API_KEY") or os.getenv("BUILT_IN_FORGE_API_KEY")
    if not api_url or not api_key:
        return _fallback()

    system = """You are Mza AI, the friendly on-page shopping assistant for Mzazi Electronics in Kenya. Before answering, use the website knowledge and current catalogue supplied below as your source of truth. Be concise: 2–5 short sentences, with bullets when useful. Help customers discover products, compare categories, understand the ordering flow, and decide whether to contact Josiah. Never invent prices, stock counts, reviews, delivery promises, a physical address, warranties, or product specifications. When a requested fact is unavailable, say it needs confirmation and offer WhatsApp. Do not claim M-Pesa is active; say it is available when configured and verified. Use Kenyan Shillings when a real price is present. Always keep the tone warm, practical, and direct. Business facts: Mzazi Electronics; owner Josiah Wasike; phone 0786163265; WhatsApp https://wa.me/254786163265; location Mukuru kwa Ruben, Embakasi South, Nairobi, Kenya; tagline Smart Electronics. Better Life.

WEBSITE KNOWLEDGE:
- The site has Home, Shop, Categories, Oraimo, Amaya, About, Contact, Account, Cart, Checkout and order-status pages.
- Customers can search and filter products, view product details, add items to a persistent cart, submit checkout details, choose WhatsApp order enquiry, and use M-Pesa when Daraja credentials are configured and verified.
- Customers can create an account, sign in, reset a password, and view account/order information.
- The admin manages genuine product names, prices, stock, categories, brands, warranty details and order statuses. Product details may show price on request or availability to confirm when the administrator has not entered those values.
- The business location is Mukuru kwa Ruben, Embakasi South, Nairobi, Kenya. Opening hours are not published.
- For live confirmation, customers can call 0786163265 or use https://wa.me/254786163265.

CATALOGUE CONTEXT:\n""" + _catalogue_context()

    safe_history = []
    for item in (history or [])[-6:]:
        role = item.get("role") if isinstance(item, dict) else None
        content = item.get("content") if isinstance(item, dict) else None
        if role in {"user", "assistant"} and content:
            safe_history.append({"role": role, "content": str(content)[:700]})
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, *safe_history, {"role": "user", "content": message}],
        "max_tokens": 420,
    }
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("error"):
            return _fallback()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return content or _fallback()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, KeyError, IndexError):
        return _fallback()
