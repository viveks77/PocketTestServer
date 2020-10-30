from django.contrib import admin
from quiz.models import Quiz, Question, Answer, UserAnswer, UserQuiz
# Register your models here.

class QuizCustom(admin.ModelAdmin):
    list_display = ("title", "owner", "class_no", "subject", "total_marks", "timestamp")
    list_filter = ("owner", "class_no", "subject", "timestamp")


class UserQuizCustom(admin.ModelAdmin):
    list_display = ("name", "user", "quiz", "score", "completed", "timestamp")
    list_filter = ("user", "quiz", "score", "completed", "timestamp")
    
    def name(self, obj):
        return obj.user.name


admin.site.register(Quiz, QuizCustom)
admin.site.register(UserQuiz, UserQuizCustom)