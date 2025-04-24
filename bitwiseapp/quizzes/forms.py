from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
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


# class BaseQuestionFormset(BaseInlineFormSet): 
    
#     def add_fields(self, form, index): 
#         super().add_fields(form, index) 

#         form.nested = AnswerFormSet(
#             instance=form.instance, 
#             data=form.data if form.is_bound else None, 
#             files=form.files if form.is_bound else None, 
#             prefix="answer-%s-%s" 
#             % (form.prefix, AnswerFormSet.get_default_prefix())
#         )

#     def is_valid(self): 
#         result = super().is_valid()

#         if self.is_bound: 
#             for form in self.forms: 
#                 if hasattr(form, "nested"): 
#                     result = result and form.nested.is_valid() 

#     def save(self, commit=True): 
#         result = super().save(commit=commit) 

#         for form in self.forms: 
#             if hasattr(form,"nested"): 
#                 form.nested.save(commit=commit) 

#         return result
    

