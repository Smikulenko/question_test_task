import pytest
from rest_framework.test import APIClient
from api.models import Question, Answer
from http import HTTPStatus
from typing import List, Dict, Any

URL = '/api/questions/'


@pytest.fixture
def api_client() -> APIClient:
    """Фикстура для клиента API"""
    return APIClient()


@pytest.fixture
def create_several_questions(db) -> List[Question]:
    """Фикстура создающая вопросы"""
    return [
        Question.objects.create(text='Кто Режиссер фильма "Паразиты"?'),
        Question.objects.create(text='Что такое ГРИП?'),
        Question.objects.create(text='Сколько книг в цикле "Колесо времени"?')
    ]


@pytest.fixture
def create_question_with_answer(db) -> Question:
    """Фикстура создающая вопросы с ответом"""
    question = Question.objects.create(text='Какие есть созвездия?')
    Answer.objects.create(question=question, text='Насос')
    Answer.objects.create(question=question, text='Ящерица')
    return question


@pytest.mark.django_db
def test_create_questions(api_client: APIClient) -> None:
    """Тест на cодание вопроса"""
    text_questions = {'text': 'Кто написал "Щегла"?'}
    response = api_client.post(URL, text_questions, format='json')

    assert response.status_code == HTTPStatus.CREATED
    assert Question.objects.count() == 1
    assert Question.objects.first().text == text_questions['text']


@pytest.mark.django_db
@pytest.mark.parametrize(
    'test_input, expected_errors',
    [
        ({'text': ''}, 'Необходимо заполнить текст вопроса.'),
        ({}, 'Поле text обязательно для заполнения.')
    ]
)
def test_create_invalid_questions(
    api_client: APIClient,
    test_input: Dict[str, Any],
    expected_errors: str,
) -> None:
    """ Проверка ошибок при создании вопроса"""
    response = api_client.post(URL, test_input, format='json')
    data = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data['text'][0] == expected_errors
    assert Question.objects.count() == 0


@pytest.mark.django_db
def test_get_question_with_answers(
    api_client: APIClient,
    create_question_with_answer: Question,
) -> None:
    """Тест на получение  вопроса с ответами"""
    question = create_question_with_answer
    response = api_client.get(f'{URL}{question.id}/', format='json')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(data['answers']) == 2


@pytest.mark.django_db
def test_delete_questions_with_answers(
    api_client: APIClient,
    create_question_with_answer: Question,
) -> None:
    """Тест на удаление вапроса с ответами"""
    question = create_question_with_answer
    response = api_client.delete(f'{URL}{question.id}/', format='json')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Question.objects.filter(id=question.id).exists()
    assert not Answer.objects.filter(question=question.id).exists()
