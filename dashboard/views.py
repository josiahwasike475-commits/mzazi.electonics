from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render
from catalog.models import Brand, Category, Product
from orders.models import Order
from django.contrib.auth import get_user_model
from .forms import SimpleBrandForm, SimpleCategoryForm, SimpleProductForm


@staff_member_required(login_url="/account/")
def dashboard(request):
    context = _dashboard_context(request)
    return render(request, "dashboard.html", context)


@staff_member_required(login_url="/account/")
def admin_panel(request):
    context = _dashboard_context(request)
    context["page_title"] = "Admin control room"
    return render(request, "admin_panel.html", context)


def _dashboard_context(request):
    user_model = get_user_model()
    return {
        "page_title": "Shop management",
        "active_nav": "dashboard",
        "metrics": {
            "sales": Order.objects.filter(payment_status="successful").aggregate(total=Sum("total"))["total"] or 0,
            "orders": Order.objects.count(),
            "pending": Order.objects.filter(status="pending").count(),
            "customers": user_model.objects.count(),
            "products": Product.objects.filter(is_active=True).count(),
            "low_stock": Product.objects.filter(is_active=True, stock_quantity__lte=3).count(),
        },
        "recent_orders": Order.objects.all()[:8],
        "low_stock_products": Product.objects.filter(is_active=True, stock_quantity__lte=3)[:6],
    }


@staff_member_required(login_url="/account/")
def simple_admin(request):
    return render(request, "simple_admin.html", {
        "products": Product.objects.filter(is_active=True)[:8],
        "categories": Category.objects.filter(is_active=True),
        "brands": Brand.objects.filter(is_active=True),
    })


def _simple_form_page(request, form_class, title, object_name, help_text, success_message):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, success_message)
        return redirect("dashboard:simple_admin")
    return render(request, "simple_admin_form.html", {"form": form, "title": title, "object_name": object_name, "help_text": help_text})


@staff_member_required(login_url="/account/")
def simple_product_add(request):
    return _simple_form_page(request, SimpleProductForm, "Add a product", "product", "Enter only the details customers need to see.", "Product saved successfully.")


@staff_member_required(login_url="/account/")
def simple_category_add(request):
    return _simple_form_page(request, SimpleCategoryForm, "Add a category", "category", "Create a clear group for your products.", "Category saved successfully.")


@staff_member_required(login_url="/account/")
def simple_brand_add(request):
    return _simple_form_page(request, SimpleBrandForm, "Add a brand", "brand", "Add a brand customers can recognise.", "Brand saved successfully.")
