from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .forms import AskForm, AnswerForm

from .models import Question


def found(request, *args, **kwargs):
    return HttpResponse('OK')


def paginate(request, objects):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 10:
        limit = 10
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(objects, limit)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def latest(request, *args, **kwargs):
    try:
        questions = Question.objects.new()
    except Question.DoesNotExist:
        raise Http404
    page_obj = paginate(request, questions)
    return render(request, 'list.html', {
        'title': 'Latest questions',
        'page_obj': page_obj,
    })


def popular(request, *args, **kwargs):
    try:
        questions = Question.objects.popular()
    except Question.DoesNotExist:
        raise Http404
    page_obj = paginate(request, questions)
    return render(request, 'list.html', {
        'title': 'Popular questions',
        'page_obj': page_obj,
    })


def question(request, *args, **kwargs):
    try:
        question = Question.objects.get(id=kwargs['pk'])
    except Question.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            _ = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    return render(request, 'question.html', {
        'question': question,
        'answers': question.answer_set.all(),
        'form': form,
        'user': request.user,
        'session': request.session
    })


def ask(request, *args, **kwargs):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {
        'title': 'Ask a question',
        'form': form,
        'user': request.user,
        'session': request.session
    })
