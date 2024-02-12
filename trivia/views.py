from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from trivia.models import Topic, Question, Answer, Trivia, TriviaQuestion
from django.utils.safestring import mark_safe
import markdown
import random

from main.wrappers import authentication_required

# Create your views here.
class TopicsView(View):
    def get(self, request):
        context = {
            'topics': Topic.objects.all().values('id', 'name')
        }
        return render(request, 'topics.html', context)
    
class TopicTriviaView(View):
    @authentication_required
    def get(self, request, topic_id=None):
        questions = Question.objects.all() if topic_id == None else Question.objects.filter(topic__id=topic_id)
        ids = [q['id'] for q in questions.values('id')]
        ids = random.sample(ids, k = 3 if len(ids) > 3 else len(ids))

        trivia = Trivia(user=request.user)
        trivia.save()
        for id in ids:
            question = Question.objects.get(id=id)
            trivia_question = TriviaQuestion(trivia=trivia, question=question)
            trivia_question.save()
        return redirect(f'/trivia/{trivia.id}')
    
class TriviaView(View):
    @authentication_required
    def get(self, request, trivia_id):
        trivia = Trivia.objects.get(id=trivia_id)
        trivia_question = TriviaQuestion.objects.filter(trivia=trivia).filter(correct_answered=None).first()
        
        if trivia_question is None:
            return redirect('/home')
        
        sentence = markdown.markdown(trivia_question.question.sentence)
        context = {
            'trivia_question_id': trivia_question.id,
            'question': {
                'sentence': mark_safe(sentence),
                'answers': Answer.objects.filter(question=trivia_question.question).values('id', 'sentence')
            }
        }
        return render(request, 'trivia.html', context)
            
    
    @authentication_required
    def post(self, request, trivia_id):
        trivia = Trivia.objects.get(id=trivia_id)
        trivia_question = TriviaQuestion.objects.filter(trivia=trivia).filter(correct_answered=None).first()
        
        if trivia_question is None:
            return redirect('/home')
        
        print(request.POST)
        sentence = markdown.markdown(trivia_question.question.sentence)
        context = {
            'trivia_question_id': trivia_question.id,
            'question': {
                'sentence': mark_safe(sentence),
                'answers': Answer.objects.filter(question=trivia_question.question).values('id', 'sentence')
            }
        }
        return render(request, 'trivia.html', context)