from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image',]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'text': 'Question Text',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
        labels = {
            'text': 'Answer Text',
            'correct': 'Is this the correct answer?',
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "topic", "number_of_questions", "image", "difficulty", "time" ]
    

AnswerFormSet = forms.inlineformset_factory(
    Question,  # Parent model
    Answer,    # Child model
    form=AnswerForm,
    extra=4,      # Number of empty forms to display initially.  Make this configurable!
    can_delete=True, # Allow deleting existing answers
)

AnswerFormSet = inlineformset_factory(Question, Answer, fields=['text', 'correct'], extra=2, can_delete=True)