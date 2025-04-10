from django.urls import path
from .views import edit_quiz, create_quiz, take_quiz, quiz_list, quiz_results, leaderboard

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', take_quiz, name='take_quiz'),
    path('attempt/<int:attempt_id>/results/', quiz_results, name='quiz_results'),
    path('create/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/edit/', edit_quiz, name='edit_quiz'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]

app_name = 'quizzes'