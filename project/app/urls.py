from django.urls import path

from .views import (
    GameListView,
    GameDetailView,
)

app_name = "game"

urlpatterns = [
    path('', GameListView.as_view(), name="list"),
    path('<int:pk>/', GameDetailView.as_view(), name="detail"),
]
