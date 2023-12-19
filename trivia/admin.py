from django.contrib import admin

from trivia.models import Topic, Question, Answer

# Register your models here.
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)