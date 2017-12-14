from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf.urls import url
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from .models import Question, Answer, Tag, Vote
from . import urls
import re

questions_per_page = 3

questions = []
for i in range(1, 30):
    questions.append({
        'title': 'title ' + str(i),
        'id': i,
        'text': 'text' + str(i),
    })

def paginate(request , qs):
    try:
        limit = int(request.GET.get('limit', 4))
    except ValueError:
        limit = 4
    if limit > 100:
        limit = 4
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    paginator.baseurl = '/?page='
    paginator.startnav = page.number - 2
    paginator.endnav = page.number + 2
    return page


def main(request):
    page = paginate(request, Question.objects.all())
    return render(request, 'index.html', {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page,})

def question(request, quest_num = 1):
    if quest_num == None:
        raise Http404("No questions provided")
    q = Question.objects.get(id=quest_num)
    page = paginate(request, q.answers.all())
    page.paginator.baseurl = '/question/' + str(quest_num) + '/?page='
    return render(request, 'pageOfOneQuestion.html', {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page, 'id': quest_num, 'question': q})

def hot(request):
    return render(request, 'thistag.html' )

def ask(request):
    return render(request, 'newquestion.html')

def signup(request):
    return render(request, 'registration.html')

def login(request):
    return render(request, 'login.html')

def tag(request, tag):
    return render(request, 'tag.html', {'tag': tag ,})

def settings(request):
    return render(request, 'settings.html')

def questions_hot(request):
    page = paginate(request, Question.objects.hot())
    page.paginator.baseurl = "questions_hot/?page="
    return render(request, "questions_hot.html", {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page,})

def questions_new(request):
    page = paginate(request, Question.objects.new())
    page.paginator.baseurl = "questions_new/?page="
    return render(request, "questions_new.html", {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page,})

def questions_tag(request, tag):
    if tag == None:
        raise Http404("No tag provided")

    page = paginate(request, Question.objects.by_tag(tag))
    if page.end_index() == 0:
        raise Http404("No tag provided")

    page.paginator.baseurl = '/tag/' + tag + '/?page='
    return render(request, "questions_tag.html", {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page, 'tag': tag})