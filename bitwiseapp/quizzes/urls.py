from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('attempt/<int:attempt_id>/results/', views.quiz_results, name='quiz_results'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]

app_name = 'quizzes'