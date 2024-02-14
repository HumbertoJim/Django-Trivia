from django.shortcuts import render
from django.views import View

from trivia.models import Trivia, TriviaQuestion


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            trivias = Trivia.objects.filter(user=request.user)
            pending = []
            finished = []
            for trivia in trivias:
                trivia_questions = TriviaQuestion.objects.filter(trivia=trivia)
                if trivia_questions.filter(correct_answered=None).exists():
                    pending.append({'id': trivia.id, 'name': trivia.name, 'number': len(pending)+1})
                else:
                    finished.append({'id': trivia.id, 'name': trivia.name, 'number': len(finished)+1})
            context = {'trivia_pending': pending, 'trivia_finished': finished}
        else:
            context = {'trivia': None}
        return render(request, 'home.html', context)