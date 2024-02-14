from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from trivia.models import Topic, Question, Answer, Trivia, TriviaQuestion
from django.utils.safestring import mark_safe
import markdown
import random

from trivia.exceptions import QuestionError, AnswerError, TriviaError
from trivia.forms import TriviaForm, TextTriviaForm, CheckTriviaForm, RadioTriviaForm
from main.wrappers import authentication_required
from main.tools import words

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
        try:
            questions = Question.objects.all() if topic_id == None else Question.objects.filter(topic__id=topic_id)
            ids = [q['id'] for q in questions.values('id')]
            ids = random.sample(ids, k = 10 if len(ids) > 10 else len(ids))
            trivia_name = "{0} {1} {2}".format(
                random.choice(words['Adjectives']),
                random.choice(words['MultidisciplinarySynonyms']) if topic_id == None else Topic.objects.get(id=topic_id).name,
                random.choice(words['TriviaSynonyms'])
            )
            trivia = Trivia(name=trivia_name, user=request.user)
            trivia.save()
            for id in ids:
                question = Question.objects.get(id=id)
                trivia_question = TriviaQuestion(trivia=trivia, question=question)
                trivia_question.save()
            return redirect(f'/trivia/{trivia.id}')
        except Trivia.DoesNotExist:
            messages.error(request, 'Invalid Trivia')
            return redirect('/home')
    
class TriviaView(View):
    @authentication_required
    def get(self, request, trivia_id):
        try:
            trivia = Trivia.objects.get(id=trivia_id)
            if trivia.user != request.user:
                raise TriviaError()
                
            trivia_question = TriviaQuestion.objects.filter(trivia=trivia).filter(correct_answered=None).first()
            if trivia_question is None:
                messages.warning(request, 'Finished')
                results = TriviaQuestion.objects.filter(trivia=trivia)
                context = {
                    'correct': results.filter(correct_answered=True).count(),
                    'total': results.count()
                }
                return render(request, 'trivia_finished.html', context)
            sentence = markdown.markdown(trivia_question.question.sentence)
            form = self._get_question_form(trivia_question.id)
            context = {
                'trivia_id': trivia_id,
                'sentence': mark_safe(sentence),
                'form': form
            }
            return render(request, 'trivia.html', context)
        except Trivia.DoesNotExist:
            messages.error(request, 'Invalid Trivia')
            return redirect('/home')
        except TriviaError:
            messages.error(request, 'Trivia Error')
            return redirect('/home')
        except TriviaQuestion.DoesNotExist:
            messages.error(request, 'Invalid Question')
            return redirect('/home')
        except QuestionError:
            messages.error(request, 'Question Error')
            return redirect('/home')
    
    
    @authentication_required
    def post(self, request, trivia_id):
        try:
            trivia = Trivia.objects.get(id=trivia_id)
            if trivia.user != request.user:
                raise TriviaError()
            
            qform = TriviaForm(request.POST)
            if not qform.is_valid():
                raise QuestionError()
            
            trivia_question = TriviaQuestion.objects.get(id=qform.cleaned_data['question_id'])

            if trivia_question.trivia != trivia:
                raise TriviaError()
            
            question = trivia_question.question
            form = self._get_question_form(trivia_question.id, request.POST)
            if form.is_valid():
                if isinstance(form, TextTriviaForm):
                    text = form.cleaned_data['answer']
                    answer = Answer.objects.get(question=question).sentence
                    trivia_question.correct_answered = answer == text.strip()
                elif isinstance(form, RadioTriviaForm):
                    answer = Answer.objects.get(id=form.cleaned_data['answer'])
                    if question != answer.question:
                        raise AnswerError()
                    trivia_question.correct_answered = answer.is_correct
                else:
                    answers = Answer.objects.filter(id__in=form.cleaned_data['answer'])
                    correct_answers = Answer.objects.filter(question=question)
                    if answers.count() != correct_answers.count():
                        trivia_question.correct_answered = False
                    else:
                        trivia_question.correct_answered = True
                        for answer in answers:
                            if answer in correct_answers:
                                trivia_question.correct_answered = False
                                break
                trivia_question.save()
                for field in form.fields.values(): # disable form
                    field.widget.attrs['disabled'] = True
                if trivia_question.correct_answered:
                    messages.success(request, 'Right!')
                else:
                    messages.error(request, 'Oops')
                template = 'trivia_answered.html'
            else:
                messages.warning(request, 'Please answer the question')
                template = 'trivia.html'
            sentence = markdown.markdown(question.sentence)
            context = {
                'trivia_id': trivia_id,
                'sentence': mark_safe(sentence),
                'form': form
            }
            return render(request, template, context)
        except Trivia.DoesNotExist:
            messages.error(request, 'Invalid Trivia')
            return redirect('/home')
        except TriviaError:
            messages.error(request, 'Trivia Error')
            return redirect('/home')
        except TriviaQuestion.DoesNotExist:
            messages.error(request, 'Invalid Question')
            return redirect('/home')
        except QuestionError:
            messages.error(request, 'Question Error')
            return redirect('/home')
        except AnswerError:
            messages.error(request, 'Answer Error')
            return redirect('/home')

    def _get_question_form(self, question_id, data=None):
        trivia_question = TriviaQuestion.objects.get(id=question_id)
        answers = Answer.objects.filter(question=trivia_question.question)
        if answers.count() == 0:
            raise QuestionError() # question has no registered answer
        if answers.filter(is_correct=True).count() == 0:
            raise QuestionError() # question has no correct answer
        initial = {'question_id': question_id} if data is None else None
        if answers.count() == 1:
            return TextTriviaForm(data=data, initial=initial)
        else:
            choices = [(answer.id, answer.sentence) for answer in answers]
            # PENDING - implement some random sort
            if answers.filter(is_correct=True).count() == 1:
                return RadioTriviaForm(choices=choices, data=data, initial=initial)
            else:
                return CheckTriviaForm(choices=choices, data=data, initial=initial)