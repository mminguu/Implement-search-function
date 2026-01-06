import uuid
from django.db import models


class SessionUser(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)


class Question(models.Model):
    user = models.ForeignKey(SessionUser, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30]


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="answer")
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30]

