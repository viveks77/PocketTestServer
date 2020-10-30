from django.db import models
from django.conf import settings
from login.models import User, Subject, Standard
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizes")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_no = models.ForeignKey(Standard, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    total_marks = models.IntegerField(default=0)
    publish_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    timestamp =  models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    content = models.CharField(max_length=256)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    content = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class UserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taken_quizzes_user")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    given_date = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class UserAnswer(models.Model):
    userquiz = models.ForeignKey(UserQuiz,  on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.content 
