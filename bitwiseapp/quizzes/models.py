from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)  # Add image field

    def __str__(self):
        return self.title

class Question(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('essay', 'Essay'),
    ]
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20, choices=QUIZ_TYPE_CHOICES, default='multiple_choice'
    )
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)  # Add image field

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text[:50]

class MultipleChoiceOption(models.Model):
    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.quiz.title}"
        else:
            return f"Guest - {self.quiz.title} (Attempt {self.id})"

class Answer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt, related_name='answers', on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(
        MultipleChoiceOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    essay_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer for {self.question.question_text[:30]}"