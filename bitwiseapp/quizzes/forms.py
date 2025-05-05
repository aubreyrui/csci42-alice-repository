from django import forms
from django.forms.models import inlineformset_factory
from django.forms import formset_factory, modelformset_factory
from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image',]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
        labels = {
            'text': 'Question Text',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }
        labels = {
            'text': 'Answer Text',
            'correct': 'Is this the correct answer?',
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "topic", "number_of_questions", "image", "difficulty", "time" ]
    
def get_question_formset(extra=1, can_delete=True):
    return modelformset_factory(Question, form=QuestionForm, extra=extra, can_delete=can_delete)

AnswerFormSet = formset_factory(AnswerForm, extra=4, can_delete=True)