from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<str:order_number>/", views.order_status, name="order_status"),
    path("api/orders/", views.create_order, name="create_order"),
    path("api/mpesa/stk-push/", views.stk_push, name="stk_push"),
    path("api/mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
]
