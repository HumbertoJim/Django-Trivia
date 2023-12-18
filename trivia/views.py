from django.shortcuts import render
from django.views import View

# Create your views here.
class Trivia(View):
    def get(self, request):
        return render(request, 'trivia.html')