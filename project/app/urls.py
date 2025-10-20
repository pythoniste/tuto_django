from django.urls import path

from .views import (
    GameListView,
    GameDetailView,
    GameUpdateView,
    GameCreateView,
    GameDeleteView,
)

app_name = "game"

urlpatterns = [
    path('', GameListView.as_view(), name="list"),
    path('<int:pk>/', GameDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', GameUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', GameDeleteView.as_view(), name="delete"),
    path('create/', GameCreateView.as_view(), name="create"),
]
