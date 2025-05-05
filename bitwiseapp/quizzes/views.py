from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponseRedirect
from .models import Quiz, Result, Question, Answer
from .forms import QuizForm, QuestionForm, AnswerFormSet, get_question_formset
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse 
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from accounts.models import Profile
from django.db import transaction
from django.core import serializers
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Quiz List view
class QuizListView(ListView):
    model = Quiz
    template_name = 'quizzes/quiz_list.html'

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quizzes/quiz_info.html'
    
def create_quiz(request):
    quiz_form = QuizForm()

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, request.FILES)
        if quiz_form.is_valid():
            quiz = Quiz()
            quiz.created_by = Profile.objects.get(user=request.user)
            quiz.topic = quiz_form.cleaned_data.get("topic")
            quiz.name = quiz_form.cleaned_data.get("name")
            quiz.number_of_questions = quiz_form.cleaned_data.get("number_of_questions")
            quiz.time = quiz_form.cleaned_data.get("time")
            quiz.difficulty = quiz_form.cleaned_data.get("difficulty")
            quiz.save()
            
            return redirect('quizzes:quiz_view', pk=quiz.pk)
        
    return render(request, 'quizzes/create_quiz.html', {'quiz_form': quiz_form})

# for deleting answer
def answer_delete(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    answer.delete()
    return redirect('quizzes:quiz_update')

# for deleting question
def question_delete(request, question_id):
    question = Question.objects.get(pk=question_id)
    question.delete()
    return redirect('quizzes:quiz_update')

# for updating questions and answers
def quiz_update(request, quiz_id, *args, **kwargs):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    existing_question_count = quiz.questions.count()
    remaining_slots = max(0, quiz.number_of_questions - existing_question_count)
    
    QuestionFormSet = get_question_formset(extra=remaining_slots, can_delete=True)

    if request.method == 'POST':
        question_formset = QuestionFormSet(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if question_formset.is_valid() and answer_formset.is_valid():
            saved_questions = []
            with transaction.atomic():
                # 1. Save existing questions first
                for question_form in question_formset:
                    if question_form.cleaned_data and question_form.instance and not question_form.cleaned_data.get('DELETE', False):
                        question = question_form.save()  # Save the existing question
                        saved_questions.append(question.instance)  # add to saved list

                # 2. Handle new questions
                for question_form in question_formset:
                    if question_form.cleaned_data and not question_form.instance and not question_form.cleaned_data.get('DELETE', False):
                        if question_form.cleaned_data and not question_form.instance and not question_form.cleaned_data.get('DELETE', False):
                            instance = question_form.save(commit=False)
                            logger.debug(f"Quiz ID: {quiz.id}")  # Debug: Check quiz ID
                            instance.quiz = quiz
                            logger.debug(f"New Question Quiz ID: {instance.quiz_id}") # Debug: Check new_question.quiz_id
                            instance.save()  # Save the new question to get an ID
                            logger.debug(f"New Question ID: {instance.id}")  # Debug: Check new question ID after saving
                            saved_questions.append(instance)  # add to saved list
                            question = instance # added

                    # 3.  Save answers for each question.
                    for answer_form in answer_formset:
                        if answer_form.cleaned_data and not answer_form.cleaned_data.get('DELETE', False):
                            answer = answer_form.save(commit=False)
                            answer.question = question
                            answer.save()

            # Handle deleted questions
            for deleted_question_form in question_formset.deleted_forms:
                if deleted_question_form.cleaned_data and deleted_question_form.instance:
                    deleted_question_form.instance.delete()
            return redirect('quizzes/quiz_info.html', pk=quiz_id)

        else:
            context = {
                'quiz': quiz,
                'question_formset': question_formset,
                'answer_formset': answer_formset,
                'max_questions': quiz.number_of_questions,
            }
            return render(request, 'quizzes/quiz_update.html', context)
    else:
        initial_question_data = quiz.questions.all()
        QuestionFormSet = get_question_formset(extra=remaining_slots, can_delete=True)
        question_formset = QuestionFormSet(queryset=initial_question_data)        
        answer_formset = AnswerFormSet()
        context = {
            'quiz': quiz,
            'question_formset': question_formset,
            'answer_formset': answer_formset,
            'max_questions': quiz.number_of_questions,
        }
        return render(request, 'quizzes/quiz_update.html', context)
    
def quiz_detail(request, quiz_id): # For running the quiz
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/detail.html', context)


# gets the detail of quiz in JSON (for checking purposes)
def quiz_detail_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for question in quiz.get_questions:
        answers = []
        for answer in question.get_answers:
            answers.append(answer.text)
        questions.append({question.text: answers})
    
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })

# saves the responses
def save_quiz_view(request, pk):
    if request.accepts("application/json"):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        questions = []

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / len(questions) 
        results = []

        for q in questions:
            a_selected = data[q.text]

            if a_selected != '':
                correct_answer = Answer.objects.filter(question=q).get(correct=True)
                if a_selected == correct_answer.text:
                    score += 1
                
                results.append({q.text: {
                    'correct_answer': correct_answer.text,
                    'answered': a_selected
                }})
            else:
                results.append({q.text: 'not answered'})

        final_score = score * multiplier


        Result.objects.create(quiz=quiz, user=user, score=final_score)

        json_response = {
            'score': final_score,
            'correct_questions': score,
            'results': results
        }   

        return JsonResponse(json_response)
    


""" class QuizCreateView(CreateView): 
     model = Quiz 
     fields = ['name', 'topic', 'number_of_questions', 'time', 'image', 'difficulty']
     template_name = "quizzes/create_quiz.html"
     def get_success_url(self): 
         return reverse('quiz_list_view') """
     
""" class QuizCreateUpdate(SingleObjectMixin, FormView):
    model = Quiz
    template_name = "quizzes/quiz_update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().post(self, request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        return BaseQuestionFormset(
            **self.get_form_kwargs(), instance=self.object
        )
    
    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Changes were saved.")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('quizzes:quiz_detail', kwargs={"pk": self.object.pk})

 """
# tried using this reference: https://swapps.com/blog/working-with-nested-forms-with-django/