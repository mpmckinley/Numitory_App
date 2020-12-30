"""Numitory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from inventory import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # MAIN
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # INVENTORY.URLS
    path('inventory/', include('inventory.urls')),

    # AUTH
    path('signup/', views.signupuser, name="signupuser"),
    path('login/', views.loginuser, name="loginuser"),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('user/<int:user_pk>/', views.edituser, name="edituser"),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

