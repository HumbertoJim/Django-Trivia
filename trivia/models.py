from django.db import models

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100)
    
class Question(models.Model):
    sentence = models.TextField()
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)

class Answer(models.Model):
    sentence = models.CharField(max_length=250)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)