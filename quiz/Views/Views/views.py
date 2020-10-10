from django.shortcuts import render, HttpResponse
from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from django.contrib.auth import get_user_model
from bootstrap_datepicker_plus import DateTimePickerInput
from django.db.models import Count

from quiz.forms import StaffRegistrationForm, UserForm, QuizAddForm, QuestionForm, BaseAnswerInlineFormset
from quiz.models import Quiz, Question, UserAnswer, Answer 

User =  get_user_model()

class StaffSignupView(CreateView):
    model = User
    form_class = StaffRegistrationForm
    template_name = 'Registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('quizList')


def staffLoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('quizList')
        else:
            return render(request,'Registration/login.html', {'error':'Incorrect Authentication credentials provided.'})
    else:
        return render(request,'Registration/login.html')


@method_decorator(staff_member_required, name='dispatch')
class UpdateUserDetailsView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "Registration/userUpdatePage.html"

    def get_success_url(self):
        return reverse('userUpdate', kwargs={'pk':self.request.user.pk})



@method_decorator(staff_member_required, name='dispatch')
class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    ordering = ("title",)
    context_object_name = 'quizes'
    template_name = 'quizList.html'

    def get_queryset(self):
        return self.request.user.quizes.all();

@method_decorator(staff_member_required, name='dispatch')
class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizAddForm
    template_name = 'quizAdd.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        return redirect('quizEdit', quiz.pk)


@method_decorator(staff_member_required, name='dispatch')
class QuizEditView(LoginRequiredMixin, UpdateView):
    model = Quiz
    form_class = QuizAddForm
    context_object_name = 'quiz'
    template_name = 'quizEdit.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answer_count=Count('answers'))
        print(self.get_object().questions)
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        return self.request.user.quizes.all()
    
    def get_success_url(self):
        return reverse('quizEdit', kwargs={'pk':self.object.pk})


@method_decorator(staff_member_required, name='dispatch')
class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quizDelete.html'
    success_url = reverse_lazy('quizList')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.request.user.quizes.all()
    

@method_decorator(staff_member_required, name='dispatch')
class QuizResultView(LoginRequiredMixin, DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quizResult.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('user').order_by('timestamp')
        extra_content = {
            'taken_quizzes':taken_quizzes
        }
        kwargs.update(extra_content)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizes.all()

@staff_member_required
@login_required
def questionAdd(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('questionEdit', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'Question/questionAdd.html', {'quiz':quiz, 'form':form})


@staff_member_required
@login_required
def questionEdit(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        formset=BaseAnswerInlineFormset,
        fields=("content","is_correct"),
        min_num=4,
        validate_min=True,
        max_num=4,
        validate_max=True
    )

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('quizEdit', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    
    return render(request, 'Question/questionEdit.html', {
        'quiz':quiz,
        'question':question,
        'form':form,
        'formset':formset
    })


@method_decorator(staff_member_required, name='dispatch')
class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'Question/questionDelete.html'
    pk_url_kwarg  = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] =  question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)
    
    def get_success_url(self):
        question = self.get_object()
        return reverse('quizEdit', kwargs={'pk':question.quiz_id})