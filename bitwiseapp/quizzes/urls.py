from django.urls import path

from .views import (
    QuizListView,
    QuizAnswerView,
    QuizInfoDetailView,
    quiz_detail_data_view,
    save_quiz_view,
    create_quiz,
    quiz_detail,
    quiz_update,
    answer_delete,
    question_delete
)

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list_view'),
    path('quiz/<pk>/info', QuizInfoDetailView.as_view(), name='quiz_view'),
    path('quiz/<pk>', QuizAnswerView.as_view(), name="quiz_answer"), # for answering the quiz
    path('quiz/<pk>/data', quiz_detail_data_view, name='quiz_data_view'), # for checking data before implementation for quiz
    path('quiz/<pk>/save', save_quiz_view, name='quiz_save_view'),
    path('create', create_quiz, name="create_quiz_view"),
    path('quiz/<quiz_id>/update', quiz_update, name='quiz_update'),
    path('quiz/<answer_id>/answer_delete', answer_delete, name='answer_delete'),
    path('quiz/<question_id>/question_delete', question_delete, name='question_delete')
]

app_name = 'quizzes'