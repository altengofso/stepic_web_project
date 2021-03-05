from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(default='', max_length=255)
    text = models.TextField(default='')
    added_at = models.DateTimeField(null=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, null=True, related_name='question_like_user')

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("question-id", kwargs={'pk': self.id})


class Answer(models.Model):
    text = models.TextField(default='')
    added_at = models.DateTimeField(null=True, auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text
