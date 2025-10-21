from rest_framework import serializers

from .models import Game, Question, Answer


# Step 1
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["name", "duration", "status", "level"]
