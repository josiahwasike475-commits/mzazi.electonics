from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.category, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("api/products/", views.products_api, name="products_api"),
    path("api/categories/", views.categories_api, name="categories_api"),
]
