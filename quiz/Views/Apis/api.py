from django.shortcuts import render
from quiz.serializers import SubjectListSerializer, QuizListSerializer, MyQuizListSerializer, QuizDetailSerializer, QuizResultSerializer, UserAnswerSerializer, UserSubmitAnswerSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions
from rest_framework import generics
from login.models import User, Subject
from quiz.models import Quiz, Question, UserAnswer, Answer, UserQuiz
import datetime

class SubjectListApi(generics.ListAPIView):
    serializer_class = SubjectListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    def get_queryset(self):
        queryset = Subject.objects.filter(class_no= self.request.user.class_no)
        return queryset


class QuizListAPI(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        subject = get_object_or_404(Subject, slug=slug)
        queryset = Quiz.objects.filter(subject=subject)
        return queryset


class MyQuizListAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = MyQuizListSerializer

    def get_queryset(self,*args, **kwargs):
        queryset = Quiz.objects.filter(taken_quizzes__user = self.request.user)
        return queryset


class QuizDetailAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = QuizDetailSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        quiz = get_object_or_404(Quiz, pk=pk)
        last_question = None
        return Response({'quiz': self.get_serializer(quiz, context={'request':self.request}).data})


class SubmitQuizAPI(generics.GenericAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        quiz = Quiz.objects.get(pk=pk)
        userquiz, created = UserQuiz.objects.get_or_create(user=self.request.user,  quiz=quiz)
        if userquiz.completed:
            return Response({
                "message":"This quiz is already given"
            })
        
        score = 0
        answers_array = request.data['answers']
        print(type(request.data['answers']))
        for ans in answers_array:
            question_id = ans['question']
            answer_id = ans['answer']

            question = get_object_or_404(Question, id=question_id)
            answer = get_object_or_404(Answer, id=answer_id)

            if answer.is_correct:
                score = score + question.marks
            
            useranswer, created = UserAnswer.objects.get_or_create(userquiz=userquiz, question=question, answer=answer)
        
        userquiz.score = score
        userquiz.completed = True
        userquiz.given_date = datetime.datetime.now()
        userquiz.save()
        
        return Response(self.get_serializer(quiz).data)


class GetUserAnswer(generics.GenericAPIView):
    serializer_class = UserSubmitAnswerSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        userquiz = UserQuiz.objects.get(quiz=pk)
        return Response(self.get_serializer(userquiz).data)
        