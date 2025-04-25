from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Quiz, Question, Answer

def is_empty_form(form):
    """
    A form is considered empty if it passes its validation,
    but doesn't have any data.

    This is primarily used in formsets, when you want to
    validate if an individual form is empty (extra_form).
    """
    if form.is_valid() and not form.cleaned_data:
        return True
    else:
        # Either the form has errors (isn't valid) or
        # it doesn't have errors and contains data.
        return False


def is_form_persisted(form):
    """
    Does the form have a model instance attached and it's not being added?
    e.g. The form is about an existing Book whose data is being edited.
    """
    if form.instance and not form.instance._state.adding:
        return True
    else:
        # Either the form has no instance attached or
        # it has an instance that is being added.
        return False

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image',]

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "topic", "number_of_questions", "image", "difficulty", "time" ]
    

AnswerFormSet = inlineformset_factory(Question, Answer, fields=['text', 'correct'], extra=2, can_delete=True)
QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, extra=2, can_delete=True)

class BaseQuestionFormset(BaseInlineFormSet): 
    
    def add_fields(self, form, index): 
         super().add_fields(form, index) 

         form.nested = AnswerFormSet(
             instance=form.instance, 
             data=form.data if form.is_bound else None, 
             files=form.files if form.is_bound else None, 
             prefix="answer-%s-%s" 
             % (form.prefix, AnswerFormSet.get_default_prefix())
         )

    def is_valid(self): 
         result = super().is_valid()

         if self.is_bound: 
             for form in self.forms: 
                 if hasattr(form, "nested"): 
                     result = result and form.nested.is_valid()

    def clean(self):
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue
            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(
                        "You are trying to add an answer to a question which" \
                        "does not exist yet. Please add information about the" \
                        "question again."
                    ),
                )


    def save(self, commit=True): 
         result = super().save(commit=commit) 

         for form in self.forms: 
             if hasattr(form,"nested"): 
                 form.nested.save(commit=commit) 

         return result
