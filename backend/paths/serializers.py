from rest_framework import serializers

from .quiz_data import PATH_CODES


class SubmitAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    question_number = serializers.IntegerField(min_value=1, max_value=9)
    answer = serializers.ChoiceField(choices=["A", "B", "C", "D", "E"])


class CompleteQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()


class SelectPathSerializer(serializers.Serializer):
    path_code = serializers.ChoiceField(choices=PATH_CODES)
