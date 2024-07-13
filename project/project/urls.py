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
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from app.views import HomeView, GameViewSet, QuestionViewSet, AnswerViewSet
from .ninja import api

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('game/', include("app.urls")),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path(r'rosetta/', include('rosetta.urls')),
    path('api-drf/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-ninja/', api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
