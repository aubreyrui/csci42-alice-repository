from django import forms
from django.forms.models import inlineformset_factory
from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image',]

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "topic", "number_of_questions", "image", "difficulty", ]
    

AnswerFormSet = inlineformset_factory(Question, Answer, fields=['text', 'correct'], extra=2, can_delete=True)
QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, extra=2, can_delete=True)
