from django.urls import path, include
from quiz.Views.Views import views
from django.contrib.auth.views import LogoutView
from quiz.Views.Apis import api

urlpatterns=[
    path('staff/', include([
        path('verification',views.StaffVerification.as_view(), name="staffverify"),
        path('quizlist', views.QuizListView.as_view(), name='quizList'),
        path('quiz/add',views.QuizCreateView.as_view(), name='quizAdd'),
        path('quiz/<int:pk>/',views.QuizEditView.as_view(), name='quizEdit'),
        path('quiz/<int:pk>/delete', views.QuizDeleteView.as_view(), name="quizDelete"),
        path('quiz/<int:pk>/results', views.QuizResultView.as_view(), name="quizResult"),
        path('quiz/<int:pk>/question/add', views.questionAdd, name="questionAdd"),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', views.questionEdit, name='questionEdit'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='questionDelete'),
        path('logout', LogoutView.as_view(), name='logout'),
        path('userupdate/<int:pk>/', views.UpdateUserDetailsView.as_view(), name='userUpdate'),
    ])),
    path('user/', include([
        path('getsubject', api.SubjectListApi.as_view()),
        path('<slug:slug>/getquiz',api.QuizListAPI.as_view()),
        path('quiz/<int:pk>/', api.QuizDetailAPI.as_view()),
        path('<slug:slug>/myquiz',api.MyQuizListAPI.as_view()),
        path('quiz/<int:pk>/submit/',api.SubmitQuizAPI.as_view()),
        path('quiz/<int:pk>/getanswers/',api.GetUserAnswer.as_view()),
    ])),
    path('ajax/load-subjects/', views.load_subjects, name="ajax_load_subjects")
]