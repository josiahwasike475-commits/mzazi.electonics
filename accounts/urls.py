from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("account/", views.account, name="account"),
    path("account/register/", views.register, name="register"),
]
