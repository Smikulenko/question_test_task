import pytest
from rest_framework.test import APIClient
from api.models import Question, Answer
from http import HTTPStatus
from typing import Dict, Any


URL_QUESTION = '/api/questions/'
URL_ANSWER = '/api/answers/'


@pytest.fixture
def api_client() -> APIClient:
    """Фикстура для клиента API"""
    return APIClient()


@pytest.fixture
def create_question(db) -> Question:
    """ Фикстура создающия вопрос"""
    question = Question.objects.create(text='Какие есть простые числа?')
    return question


@pytest.fixture
def create_question_with_answers(db) -> Question:
    """ Фикстура создающия вопросы с ответами"""
    question = Question.objects.create(text='Произведения Чехова?')
    Answer.objects.create(question=question, text='Дама с собачкой')
    Answer.objects.create(question=question, text='Человек в футляре')
    return question


@pytest.mark.django_db
def tests_add_answer(api_client: APIClient, create_question: Question) -> None:
    """ Тест на создание ответа на вопрос"""
    question = create_question
    url = f'{URL_QUESTION}{question.id}/answers/'
    text_answers = {'text': '2'}
    response = api_client.post(url, text_answers, format='json')
    data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert Answer.objects.filter(question=question).count() == 1
    assert data['text'] == text_answers['text']


@pytest.mark.django_db
@pytest.mark.parametrize(
    'test_input, expected_errors',
    [
        ({'text': ''}, 'Необходимо заполнить текст ответа.'),
        ({}, 'Поле text обязательно для заполнения.')
    ]
)
def test_create_invalid_answers(
    api_client: APIClient,
    test_input: Dict[str, Any],
    expected_errors: str,
    create_question: Question,
) -> None:
    """ Проверка ошибок при создании ответа"""
    question = create_question
    url = f'{URL_QUESTION}{question.id}/answers/'
    response = api_client.post(url, test_input, format='json')
    data = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data['text'][0] == expected_errors
    assert Answer.objects.filter(question=question).count() == 0


@pytest.mark.django_db
def test_several_answers_same_user(
    api_client: APIClient,
    create_question: Question,
) -> None:
    """ Тест на  возможность несколько ответов от одного пользователя"""
    question = create_question
    url = f'{URL_QUESTION}{question.id}/answers/'
    user_id = '883765231e3d4e0da8bfcc992d8bcc08'

    text_answers_first = {'text': '2', 'user_id': user_id}
    text_answers_second = {'text': '3', 'user_id': user_id}

    response_first = api_client.post(url, text_answers_first, format='json')
    response_second = api_client.post(url, text_answers_second, format='json')

    assert response_first.status_code == HTTPStatus.CREATED
    assert response_second.status_code == HTTPStatus.CREATED
    assert Answer.objects.filter(question=question).count() == 2


@pytest.mark.django_db
def test_create_answer_to_nonexistent_question(api_client: APIClient) -> None:
    """ Тест на создание ответа к несуществующему вопросу"""
    url = f'{URL_QUESTION}999/answers/'
    text_answers = {'text': 'Ответ'}
    response = api_client.post(url, text_answers, format='json')

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_get_answer(
    api_client: APIClient,
    create_question_with_answers: Question,
) -> None:
    """ Тест на получение ответа"""
    question = create_question_with_answers
    answer = question.answers.first()
    response = api_client.get(f'{URL_ANSWER}{answer.id}/', format='json')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data['text'] == answer.text


@pytest.mark.django_db
def test_delete_answer(
    api_client: APIClient,
    create_question_with_answers: Question,
) -> None:
    """ Тест на удаление ответа"""
    question = create_question_with_answers
    answer = question.answers.first()
    response = api_client.delete(f'{URL_ANSWER}{answer.id}/', format='json')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Answer.objects.filter(id=answer.id).exists()
    assert Answer.objects.filter(question=question).count() == 1
