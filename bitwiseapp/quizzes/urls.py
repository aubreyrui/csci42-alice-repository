from django.urls import path

from .views import (
    QuizListView,
    QuizDetailView,
    quiz_detail_data_view,
    save_quiz_view,
    create_quiz
)

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list_view'),
    path('quiz/<pk>', QuizDetailView.as_view(), name='quiz_view'),
    path('quiz/<pk>/data', quiz_detail_data_view, name='quiz_data_view'),
    path('quiz/<pk>/save', save_quiz_view, name='quiz_save_view'),
    path('create', create_quiz, name="create_quiz_view"),
]

app_name = 'quizzes'