from django import forms
from .models import Quiz, Question, MultipleChoiceOption

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'image']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'order', 'image']

class MultipleChoiceOptionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceOption
        fields = ['text', 'is_correct']

class EssayQuestionForm(forms.Form):
    essay_answer = forms.CharField(widget=forms.Textarea)