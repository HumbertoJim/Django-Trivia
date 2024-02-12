from django.contrib import admin

from trivia.models import Topic, Question, Answer, Trivia, TriviaQuestion

# Register your models here.
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)

admin.site.register(Trivia)
admin.site.register(TriviaQuestion)