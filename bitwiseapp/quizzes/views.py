from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Quiz, Question, MultipleChoiceOption, QuizAttempt, Answer
from .forms import QuizForm, QuestionForm, EssayQuestionForm, MultipleChoiceOptionForm

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    if request.method == 'POST':
        attempt = QuizAttempt.objects.create(quiz=quiz, user=request.user if request.user.is_authenticated else None, total_questions=questions.count())
        score = 0
        for question in questions:
            answer = None
            if question.question_type == 'multiple_choice':
                selected_option_id = request.POST.get(f'question_{question.id}')
                if selected_option_id:
                    try:
                        selected_option = MultipleChoiceOption.objects.get(pk=selected_option_id, question=question)
                        Answer.objects.create(attempt=attempt, question=question, selected_option=selected_option)
                        if selected_option.is_correct:
                            score += 1
                    except MultipleChoiceOption.DoesNotExist:
                        Answer.objects.create(attempt=attempt, question=question)
            elif question.question_type == 'essay':
                essay_text = request.POST.get(f'essay_{question.id}', '')
                Answer.objects.create(attempt=attempt, question=question, essay_answer=essay_text)

        attempt.score = score
        attempt.end_time = timezone.now()
        attempt.save()
        return redirect('quiz_results', attempt_id=attempt.id)
    else:
        form_dict = {}
        for question in questions:
            if question.question_type == 'essay':
                form_dict[question.id] = EssayQuestionForm(prefix=f'essay_{question.id}')
        return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions, 'essay_forms': form_dict})

def quiz_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, pk=attempt_id)
    answers = Answer.objects.filter(attempt=attempt).select_related('question', 'selected_option')
    return render(request, 'quizzes/quiz_results.html', {'attempt': attempt, 'answers': answers})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'form': form})

@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if quiz.created_by != request.user:
        messages.error(request, 'You are not authorized to edit this quiz.')
        return redirect('quiz_list')

    QuestionFormSet = inlineformset_factory(
        Quiz, Question, form=QuestionForm, extra=1, can_delete=True
    )
    MultipleChoiceOptionFormSet = inlineformset_factory(
        Question, MultipleChoiceOption, form=MultipleChoiceOptionForm, extra=2, can_delete=True
    )

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, request.FILES, instance=quiz)  # Handle files
        question_formset = QuestionFormSet(request.POST, request.FILES, instance=quiz, prefix='questions') # Handle files

        mc_option_formset = {}
        for i, question_form in enumerate(question_formset):
            if question_form.instance.question_type == 'multiple_choice':
                mc_option_formset[question_form.instance.id] = MultipleChoiceOptionFormSet(
                    request.POST, request.FILES, instance=question_form.instance, prefix=f'options_{question_form.instance.id}' # Handle files
                )
            else:
                mc_option_formset[question_form.instance.id] = None

        if quiz_form.is_valid() and question_formset.is_valid() and all(fs is None or fs.is_valid() for fs in mc_option_formset.values()):
            quiz_form.save()
            question_formset.save()
            for fs in mc_option_formset.values():
                if fs:
                    fs.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quiz_list')
    else:
        quiz_form = QuizForm(instance=quiz)
        question_formset = QuestionFormSet(instance=quiz, prefix='questions')
        mc_option_formset = {}
        for question in quiz.questions.all():
            if question.question_type == 'multiple_choice':
                mc_option_formset[question.id] = MultipleChoiceOptionFormSet(instance=question, prefix=f'options_{question.id}')
            else:
                mc_option_formset[question.id] = None

    return render(
        request,
        'quizzes/edit_quiz.html',
        {
            'quiz_form': quiz_form,
            'question_formset': question_formset,
            'mc_option_formset': mc_option_formset,
            'quiz': quiz,
        },
    )

@login_required
def leaderboard(request):
    leaderboard_data = (
        QuizAttempt.objects.filter(user__isnull=False)
        .values('user__username')
        .annotate(total_score=models.Sum('score'))
        .order_by('-total_score')
    )
    return render(request, 'quizzes/leaderboard.html', {'leaderboard': leaderboard_data})