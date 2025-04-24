from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from .models import Quiz, Result, Question, Answer
from .forms import QuizForm, QuestionFormSet
from django.shortcuts import render, redirect
from django.urls import reverse 

# Quiz List view
class QuizListView(ListView):
    model = Quiz
    template_name = 'quizzes/quiz_list.html'

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quizzes/detail.html'

# class QuizCreateView(CreateView): 
#     model = Quiz 
#     fields = ['name', 'topic', 'number_of_questions', 'time', 'image', 'difficulty']

#     def get_context_data(self, **kwargs): 
#         data = super().get_context_data(**kwargs) 
#         if self.request.POST: 
#             data['questions'] = QuestionFormSet(self.request.POST) 
#         else: 
#             data['questions'] = QuestionFormSet()

#     def form_valid(self, form): 
#         context = self.get_context_data() 
#         questions = context['questions'] 
#         self.object = form.save() 
#         if questions.is_valid(): 
#             questions.instance = self.object 
#             questions.save() 
#         return super().form_valid(form)
    
#     def get_success_url(self): 
#         return reverse('quiz_list_view')

# tried using this reference: https://swapps.com/blog/working-with-nested-forms-with-django/
    

def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST) # Assuming you have a Quiz instance
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()
            question_formset.instance = quiz
            question_formset.save()
            return redirect('quiz_detail', quiz.id)
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet()
    return render(request, 'quizzes/create_quiz.html', {'quiz_form': quiz_form, 'question_formset': question_formset})

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