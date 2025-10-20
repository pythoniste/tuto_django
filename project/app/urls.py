from django.urls import path

from .views import (
    GameListView,
)

app_name = "game"

urlpatterns = [
    path('', GameListView.as_view(), name="list"),
]
