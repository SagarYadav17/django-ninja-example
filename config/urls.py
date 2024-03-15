from django.contrib import admin
from django.urls import path
from authentication.views import api as auth_api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", auth_api.urls),
]
