import uuid
from django.db import models


# Create your models here.
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    username = models.CharField(max_length=200, unique=True)
    total = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Quizzes'
        
    def __str__(self):
        return f"{self.username} | {str(self.score)}"


class Question(models.Model):
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Choice(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey(to=Question, related_name='choice_question', on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAnswer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(to=Choice, on_delete=models.CASCADE)
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.question.text + " |  " + self.choice.text + " | " + str(self.answer)
