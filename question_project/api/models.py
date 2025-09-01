import uuid
from django.db import models


class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    user_id = models.UUIDField(default=uuid.uuid4)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
