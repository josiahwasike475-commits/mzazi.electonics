from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("", include("catalog.urls")),
    path("", include("orders.urls")),
    path("", include("accounts.urls")),
    path("", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT})]
