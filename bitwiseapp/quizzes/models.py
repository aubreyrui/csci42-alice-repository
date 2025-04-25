from django.db import models
from django.urls import reverse

from accounts.models import Profile

# Create your models here.

DIFFICULTY_CHOICES = (
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Hard", "Hard"),
)


class Topic(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="Programming", blank=True, null=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=60)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quiz")
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    image = models.ImageField(null=True, blank=True)
    created_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="quiz"
    )
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    difficulty = models.CharField(
        help_text="The difficulty of the quiz", max_length=6, choices=DIFFICULTY_CHOICES
    )

    def __str__(self):
        return f"{self.name} - {self.topic}"

    def get_absolute_url(self):
        return reverse("quizzes:quiz_view", args=[self.pk])

    @property
    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    text = models.CharField(max_length=120)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {str(self.text)[:10]}"

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    @property
    def get_answers(self):
        return self.answers.all()


class Answer(models.Model):
    text = models.CharField(max_length=120)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {str(self.question.text)[:15]}, answer: {str(self.text)[:10]}, correct: {self.correct}"


class Result(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.pk)
