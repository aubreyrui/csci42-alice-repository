from django import forms
from django.contrib import admin

from .models import (Quiz, Question, Answer, Result, Topic)

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionInLine(admin.TabularInline):
    model = Question

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['name', 'topic', 'created_by', 'difficulty']
    list_filter = ['topic']

class TopicnAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ['name', 'description']

class ResultAdmin(admin.ModelAdmin):
    model = Result
    list_display = ['date', 'quiz', 'user']

class QuizAdmin(admin.ModelAdmin):
    model = Quiz
    inlines = [QuestionInLine]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

    

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result, ResultAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Topic, TopicnAdmin)