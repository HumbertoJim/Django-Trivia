from django.db import models
from accounts.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.id} - {self.name}'
    
class Question(models.Model):
    sentence = models.TextField()
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.id} - {self.sentence} ({self.topic.name})'

class Answer(models.Model):
    sentence = models.CharField(max_length=250)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.id} - {self.sentence} ({self.question.sentence})'
    

class Trivia(models.Model):
    name = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.user.username}'

class TriviaQuestion(models.Model):
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct_answered = models.BooleanField(default=None, null=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.trivia.user.username} ({self.question.sentence})'