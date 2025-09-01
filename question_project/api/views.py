import uuid
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer, QuestionAnswerSerializer


class QustionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ['get', 'post', 'delete']

    @action(
        methods=['post'],
        detail=True,
        url_path='answers',
        url_name='answers'
    )
    def add_answer(self, request, pk=None):
        question = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            question=question,
            user_id=request.data.get('user_id', uuid.uuid4())
        )
        return Response(serializer.data, status=201)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionAnswerSerializer
        return QuestionSerializer


class AnswerViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
