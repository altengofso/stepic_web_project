from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User

from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        pass

    def save(self):
        question = Question(**self.cleaned_data)
        if self._user.id is not None:
            question.author = self._user
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question

    def clean(self):
        pass

    def save(self):
        answer = Answer(**self.cleaned_data)
        if self._user.id is not None:
            answer.author = self._user
        answer.save()
        return answer


class SignupForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(
        required=False,
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('Email is already in use')
        except User.DoesNotExist:
            pass
        return email

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_cache = authenticate(username=username, password=password)
        if user_cache is not None:
            if user_cache.is_active:
                pass
            else:
                raise forms.ValidationError('This account is inactive.')
        else:
            raise forms.ValidationError('''Please enter a correct username and password. 
            Note that both fields may be case-sensitive.''')

