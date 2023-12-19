from django.shortcuts import render
from django.views import View

from trivia.models import Trivia

class Home(View):
    def get(self, request):
        trivia = Trivia.objects.filter(user=request.user)
        if trivia.exists():
            trivia = trivia.last()
        else:
            trivia = None
        context = {'trivia': trivia}
        return render(request, 'home.html', context)