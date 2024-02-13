from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from trivia.models import Topic, Question, Answer, Trivia, TriviaQuestion
from django.utils.safestring import mark_safe
import markdown
import random

from trivia.forms import TriviaForm, TextTriviaForm, CheckTriviaForm, RadioTriviaForm
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

        form = self._get_question_form(trivia_id)
        context = {
            'trivia_id': trivia_id,
            'sentence': mark_safe(sentence),
            'form': form
        }
        return render(request, 'trivia.html', context)
    
    
    @authentication_required
    def post(self, request, trivia_id):
        qform = TriviaForm(request.POST)
        if not qform.is_valid():
            raise TriviaQuestion.DoesNotExist()
        form = self._get_question_form(qform.cleaned_data['question_id'], request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            print(answer)
            # continue here
        return redirect(f'/trivia/{trivia_id}')

    def _get_question_form(self, question_id, data=None):
        trivia_question = TriviaQuestion.objects.get(id=question_id)
        answers = Answer.objects.filter(question=trivia_question.question)
        if answers.count() == 0:
            raise TriviaQuestion.DoesNotExist()
        if answers.filter(is_correct=True).count() == 0:
            raise TriviaQuestion.DoesNotExist()
        initial = {'question_id': question_id} if data is None else None
        if answers.count() == 1:
            return TextTriviaForm(data=data, initial=initial)
        else:
            choices = [(answer.id, answer.sentence) for answer in answers]
            if answers.filter(is_correct=True).count() == 1:
                return RadioTriviaForm(choices=choices, data=data, initial=initial)
            else:
                return CheckTriviaForm(choices=choices, data=data, initial=initial)
