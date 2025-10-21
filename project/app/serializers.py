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
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ["text", "points", "order"]
#
#
# class GameSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Game
#         fields = ["name", "duration", "status", "level", "question_set"]


# Step 4
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ["text", "points", "order"]
#
#
# class GameSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Game
#         depth = 2
#         fields = ["name", "duration", "status", "level", "question_set"]


# Step 5
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["text", "points", "order"]


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        depth = 2
        fields = ["text", "points", "order", "answer_set"]


class GameSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        depth = 3
        fields = ["name", "duration", "status", "level", "question_set"]
