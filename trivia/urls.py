from django.urls import path

from trivia.views import TopicsView, TriviaView, TopicTriviaView

urlpatterns = [
    path('<int:trivia_id>', TriviaView.as_view(), name='trivia'),
    path('topics', TopicsView.as_view(), name='topics'),
    path('topics/<int:topic_id>', TopicTriviaView.as_view(), name='topic_trivia'),
    #path('question/<int:trivia_question_id>')
]