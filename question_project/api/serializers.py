from rest_framework import serializers
from .models import Answer, Question


class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'blank': 'Необходимо заполнить текст вопроса.',
            'required': 'Поле text обязательно для заполнения.'
        }
    )

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at',]


class AnswerSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'blank': 'Необходимо заполнить текст ответа.',
            'required': 'Поле text обязательно для заполнения.'
        }
    )

    class Meta:
        model = Answer
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at',]


class QuestionAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = fields = ['id', 'text', 'created_at', 'answers']
