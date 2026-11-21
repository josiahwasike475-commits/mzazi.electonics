from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("simple-admin/", views.simple_admin, name="simple_admin"),
    path("simple-admin/product/add/", views.simple_product_add, name="simple_product_add"),
    path("simple-admin/category/add/", views.simple_category_add, name="simple_category_add"),
    path("simple-admin/brand/add/", views.simple_brand_add, name="simple_brand_add"),
]
