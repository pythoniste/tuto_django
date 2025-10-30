from django.urls import path

from .views import (
    GameListView,
    GameDetailView,
    GameUpdateView,
    GameCreateView,
    GameDeleteView,
    GenreDatatableView,
    bulk_create_questions_answers,
    create_play,
    PlayUpdateView,
)

app_name = "game"

urlpatterns = [
    path('', GameListView.as_view(), name="list"),
    path('<int:pk>/', GameDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', GameUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', GameDeleteView.as_view(), name="delete"),
    path('create/', GameCreateView.as_view(), name="create"),
    path('genre/', GenreDatatableView.as_view(), name="genre"),
    path('<int:pk>/bulk-create-qr/', bulk_create_questions_answers, name='bulk_create_qr'),
    path('<int:pk>/play/create/', create_play, name="create_play"),
    path('play/<int:pk>/', PlayUpdateView.as_view(), name="play"),
]
