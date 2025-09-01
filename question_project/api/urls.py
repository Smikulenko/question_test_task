from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import AnswerViewSet, QustionViewSet

router = DefaultRouter()

router.register('questions', QustionViewSet, basename='questions')
router.register('answers', AnswerViewSet, basename='answers')

urlpatterns = [
  path('', include(router.urls))
]
