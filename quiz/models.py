import uuid
from django.db import models


# Create your models here.
class TestDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    username = models.CharField(max_length=200, unique=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} | {str(self.score)}"


class Question(models.Model):
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey(to=Question, related_name='options', on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Response(models.Model):
    question_id = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    option_id = models.ForeignKey(to=Option, on_delete=models.CASCADE)
    test_id = models.ForeignKey(to=TestDetail, on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.question_id.text + " |  " + self.option_id.text + " | " + str(self.answer)
