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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, re_path

from rest_framework import routers

from app.views import (
    HomeView,
    GameViewSet,
    QuestionViewSet,
    AnswerViewSet,
)
from example.views import (
    LoginView as CustomLoginView,
    LogoutView as CustomLogoutView,
    login_view,
    logout_view,
)

from .ninja import api
from .views import test_celery


router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)


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
    path('i18n/', include('django.conf.urls.i18n')),
    *i18n_patterns(path('admin/', admin.site.urls)),
    path('api-ninja/', api.urls),
    path('martor/', include('martor.urls')),
    path('health/', include('health_check.urls')),
]

if 'rest_framework' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('api-drf/', include(router.urls)),
        path('api-auth/', include('rest_framework.urls')),
    ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('test-celery/', test_celery, name='test_celery'),
    ]
