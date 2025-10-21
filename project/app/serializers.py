from rest_framework import serializers

from .models import Game, Question, Answer


# Step 1
# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = ["name", "duration", "status", "level"]


# Step 2
# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = ["name", "duration", "status", "level", "question_set"]


# Step 3
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["text", "points", "order"]


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ["name", "duration", "status", "level", "question_set"]
