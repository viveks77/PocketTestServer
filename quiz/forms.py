from django import forms
from django.forms import widgets, ModelForm, BaseInlineFormSet
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.utils import ValidationError
from bootstrap_datepicker_plus import DateTimePickerInput
from login.models import User, Subject
from quiz.models import Quiz, Question, Answer, UserAnswer

#Staff registration form
class StaffRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'class_no', 'subject', 'mobile_no', 'location')
    
    def __init__(self, *args, **kwargs):
        super(StaffRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset= Subject.objects.none()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        if 'class_no' in self.data:
            try:
                class_id = int(self.data.get('class_no'))
                self.fields['subject'].queryset = Subject.objects.filter(class_no=class_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fileds['subject'].queryset = self.instance.class_no.subject_set
        

    def save(self, commit=True):
        user = super(StaffRegistrationForm, self).save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("name", "class_no", "mobile_no", "location")
        widgets = {
            'name': widgets.TextInput(attrs={'class':'form-control'}),
            'class_no': widgets.Select(attrs={'class':'form-control'}),
            'mobile_no': widgets.NumberInput(attrs={'class':'form-control'}),
            'location': widgets.TextInput(attrs={'class':'form-control'}),
        }



class QuizAddForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ("title", "description", "publish_date", "end_date")
        widgets = {
            'title': widgets.TextInput(attrs={'class':'form-control'}),
            'description': widgets.TextInput(attrs={'class':'form-control'}),
            'publish_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }




class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('content', 'marks',)
        widgets = {
            'content': widgets.TextInput(attrs={'class':'form-control'}),
            'marks': widgets.NumberInput(attrs={'class':'form-control'}),
        }


class BaseAnswerInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
    
        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get("DELETE", False):
                if form.cleaned_data.get("is_correct", False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError("mark atleast one correct answer",code="no_correct_answer")