from datetime import timedelta
from ninja import Schema

from .enums import GameStatus, GameLevel

class AnswerSchema(Schema):
    text: str
    points: int
    order: int


class QuestionSchema(Schema):
    text: str
    points: int
    order: int
    answer_set: list[AnswerSchema]


class GameSchema(Schema):
    name: str
    duration: timedelta
    status: GameStatus
    level: GameLevel
    question_set: list[QuestionSchema]
