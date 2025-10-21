"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, re_path

from app.views import HomeView
from example.views import (
    LoginView as CustomLoginView,
    LogoutView as CustomLogoutView,
    login_view,
    logout_view,
)


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='login_bis'),
    path('logout/', LogoutView.as_view(), name='logout_bis'),
    path('custom/login/', CustomLoginView.as_view(), name='login_ter'),
    path('custom/logout/', CustomLogoutView.as_view(), name='logout_ter'),
    path('func/login/', login_view, name='login_ter'),
    path('func/logout/', logout_view, name='logout_ter'),
    path('game/', include("app.urls")),
    path('admin/', admin.site.urls),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
