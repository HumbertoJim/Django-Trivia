from django.contrib import admin

from trivia.models import Topic, Question, Answer

# Register your models here.
admin.register(Topic)
admin.register(Question)
admin.register(Answer)