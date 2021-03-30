from django.contrib import admin
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.LoginView.as_view(), name="login"),
]
