from django.urls import path

from trivia.views import Trivia

urlpatterns = [
    path('', Trivia.as_view(), name='trivia')
]