from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_payload(product):
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "brand": product.brand.name if product.brand else "MZAZI",
        "category": product.category.name,
        "category_slug": product.category.slug,
        "description": product.description,
        "price": float(product.price) if product.price is not None else None,
        "compare_at_price": float(product.compare_at_price) if product.compare_at_price is not None else None,
        "stock": product.stock_quantity,
        "in_stock": product.in_stock,
        "image_url": product.image_url,
        "is_demo": product.is_demo,
        "is_featured": product.is_featured,
        "is_new": product.is_new,
        "is_best_seller": product.is_best_seller,
        "popularity": product.popularity,
        "warranty": product.warranty,
        "specs": product.technical_specs,
        "url": product.get_absolute_url(),
    }


def catalogue_context(products=None, **extra):
    products = products if products is not None else Product.objects.filter(is_active=True).select_related("brand", "category")
    return {
        "products": [product_payload(product) for product in products],
        "categories": list(Category.objects.filter(is_active=True).values("name", "slug", "description", "accent")),
        **extra,
    }


def shop(request):
    return render(request, "shop.html", catalogue_context(page_title="Shop all electronics", active_nav="shop"))


def category(request, slug):
    category_obj = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category_obj, is_active=True).select_related("brand", "category")
    active_nav = category_obj.slug if category_obj.slug in {"oraimo", "amaya", "lights"} else "categories"
    return render(request, "shop.html", catalogue_context(products, page_title=category_obj.name, category=category_obj, category_slug=category_obj.slug, active_nav=active_nav))


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("brand", "category"), slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    context = catalogue_context([product, *related], product=product_payload(product), related_products=[product_payload(p) for p in related], page_title=product.name)
    return render(request, "product_detail.html", context)


def products_api(request):
    products = Product.objects.filter(is_active=True).select_related("brand", "category")
    return JsonResponse({"products": [product_payload(product) for product in products]})


def categories_api(request):
    return JsonResponse({"categories": list(Category.objects.filter(is_active=True).values("name", "slug", "description", "accent"))})
