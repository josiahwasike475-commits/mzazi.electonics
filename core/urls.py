from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("manus-routes.json", views.routes_manifest, name="routes_manifest"),
    path("api/assistant/", views.assistant_api, name="assistant_api"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("newsletter/", views.newsletter, name="newsletter"),
]
